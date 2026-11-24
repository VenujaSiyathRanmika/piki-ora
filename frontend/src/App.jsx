
import { useCallback, useEffect, useState } from "react";
import Login from "./Login";
import AdminLogin from "./AdminLogin";
import AdminDashboard from "./AdminDashboard";
import api from "./api";
import "./App.css";

const API = {
  doctors: "/doctors/api/",
  login: "/api/accounts/login/",
  adminLogin: "/api/accounts/admin-login/",
  slots: "/api/appointments/slots/",
  appointments: "/api/appointments/my/",
  csrf: "/api/accounts/csrf/",
  logout: "/api/accounts/logout/",
};

function App() {
  const [doctors, setDoctors] = useState([]);
  const [slots, setSlots] = useState([]);
  const [appointments, setAppointments] = useState([]);

  const [loggedInUser, setLoggedInUser] = useState("");
  const [checkingLogin, setCheckingLogin] = useState(true);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  const [loadingDoctors, setLoadingDoctors] = useState(true);
  const [loadingSlots, setLoadingSlots] = useState(false);

  const [selectedSlot, setSelectedSlot] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const loadSlots = useCallback(async () => {
    setLoadingSlots(true);

    try {
      const response = await api.get(API.slots);
      const data = response.data;
      setSlots(Array.isArray(data) ? data : data.results || []);
    } catch {
      setError(
        "Could not load appointment slots. Check that Django is running."
      );
    } finally {
      setLoadingSlots(false);
    }
  }, []);

  const loadAppointments = useCallback(async () => {
    try {
      const response = await api.get(API.appointments);
      const data = response.data;
      setAppointments(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Could not load your appointments."
      );
    }
  }, []);

  // Load doctors and restore an existing login session.
  useEffect(() => {
    let active = true;

    api
      .get(API.doctors)
      .then((response) => {
        if (!active) return;
        const data = response.data;
        setDoctors(Array.isArray(data) ? data : data.results || []);
      })
      .catch(() => {
        if (active) {
          setError(
            "Could not load doctors. Check that Django is running."
          );
        }
      })
      .finally(() => {
        if (active) setLoadingDoctors(false);
      });

    async function checkSession() {
      try {
        const adminResponse = await api.get(API.adminLogin);

        if (
          active &&
          adminResponse.data.authenticated &&
          adminResponse.data.is_staff
        ) {
          setLoggedInUser(adminResponse.data.username);
          setIsAdmin(true);
        } else {
          const patientResponse = await api.get(API.login);

          if (
            active &&
            patientResponse.data.authenticated &&
            !patientResponse.data.is_staff
          ) {
            setLoggedInUser(patientResponse.data.username);
            setIsAdmin(false);
          }
        }
      } catch (err) {
        console.error("Session check failed:", err);
      } finally {
        if (active) setCheckingLogin(false);
      }
    }

    checkSession();

    return () => {
      active = false;
    };
  }, []);

  // Load appointment information for patients only.
  useEffect(() => {
    if (loggedInUser && !isAdmin) {
      setError("");
      loadSlots();
      loadAppointments();
    } else {
      setSlots([]);
      setAppointments([]);
    }
  }, [loggedInUser, isAdmin, loadSlots, loadAppointments]);

  async function handleBook(event) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!selectedSlot) {
      setError("Please select an appointment time.");
      return;
    }

    setSaving(true);

    try {
      await api.get(API.csrf);

      await api.post(API.appointments, {
        slot: Number(selectedSlot),
        reason: reason.trim(),
      });

      setMessage("Appointment booked successfully.");
      setSelectedSlot("");
      setReason("");

      await loadSlots();
      await loadAppointments();
    } catch (err) {
      const data = err.response?.data;
      const detail = data?.detail || data?.error;

      setError(
        typeof detail === "string"
          ? detail
          : "Booking failed. Please check the selected slot and try again."
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleCancel(appointmentId) {
    if (
      !window.confirm(
        "Are you sure you want to cancel this appointment?"
      )
    ) {
      return;
    }

    setError("");
    setMessage("");

    try {
      await api.get(API.csrf);
      await api.post(
        `/api/appointments/cancel/${appointmentId}/`
      );

      setMessage("Appointment cancelled successfully.");
      await loadSlots();
      await loadAppointments();
    } catch (err) {
      const data = err.response?.data;
      const detail = data?.detail || data?.error;

      setError(
        typeof detail === "string"
          ? detail
          : "Cancellation failed. Please try again."
      );
    }
  }

  async function handleLogout() {
    setError("");
    setMessage("");

    try {
      await api.get(API.csrf);
      await api.post(API.logout);

      setLoggedInUser("");
      setIsAdmin(false);
      setShowAdminLogin(false);
      setSelectedSlot("");
      setReason("");
      setAppointments([]);
      setSlots([]);
    } catch {
      setError("Logout failed. Please try again.");
    }
  }

  function getAppointmentSlot(appointment) {
    return (
      appointment.slot_details ||
      appointment.appointment_slot ||
      (typeof appointment.slot === "object"
        ? appointment.slot
        : null)
    );
  }

  function getAppointmentId(appointment) {
    return appointment.id;
  }

  function getDoctorName(doctor) {
    if (typeof doctor === "object" && doctor !== null) {
      return (
        doctor.name ||
        `Dr. ${doctor.first_name || ""} ${doctor.last_name || ""}`.trim()
      );
    }

    return "";
  }

  function formatDate(value) {
    if (!value) return "Date not available";

    return new Date(`${value}T00:00:00`).toLocaleDateString(
      "en-NZ",
      {
        day: "numeric",
        month: "short",
        year: "numeric",
      }
    );
  }

  function formatTime(value) {
    if (!value) return "";
    return value.slice(0, 5);
  }

  // Initial session check.
  if (checkingLogin) {
    return (
      <div className="app">
        <header className="header">
          <h1>Piki Ora Medical Centre</h1>
          <p>Healthcare for everyone</p>
        </header>
        <main className="main">
          <p>Checking login...</p>
        </main>
      </div>
    );
  }

  // Administrator dashboard.
  if (isAdmin && loggedInUser) {
    return <AdminDashboard onLogout={handleLogout} />;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Piki Ora Medical Centre</h1>
        <p>Healthcare for everyone</p>
      </header>

      <main className="main">
        {!loggedInUser && (
          <>
            {!showAdminLogin ? (
              <>
                <Login
                  onLogin={(username) => {
                    setError("");
                    setMessage("");
                    setLoggedInUser(username);
                    setIsAdmin(false);
                  }}
                />

                <div
                  style={{
                    textAlign: "center",
                    marginTop: "16px",
                    marginBottom: "20px",
                  }}
                >
                  <button
                    type="button"
                    onClick={() => {
                      setError("");
                      setMessage("");
                      setShowAdminLogin(true);
                    }}
                  >
                    Administrator Login
                  </button>
                </div>
              </>
            ) : (
              <>
                <AdminLogin
                  onLogin={(username) => {
                    setError("");
                    setMessage("");
                    setLoggedInUser(username);
                    setIsAdmin(true);
                    setShowAdminLogin(false);
                  }}
                />

                <div
                  style={{
                    textAlign: "center",
                    marginTop: "16px",
                    marginBottom: "20px",
                  }}
                >
                  <button
                    type="button"
                    onClick={() => {
                      setError("");
                      setShowAdminLogin(false);
                    }}
                  >
                    Back to Patient Login
                  </button>
                </div>
              </>
            )}
          </>
        )}

        {loggedInUser && (
          <div className="login-status">
            <div>
              <strong>Welcome, {loggedInUser}</strong>
              <p>Manage your healthcare appointments below.</p>
            </div>
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}

        {message && (
          <div className="app-message success-message">
            {message}
          </div>
        )}

        {error && (
          <div className="app-message error-message">
            {error}
          </div>
        )}

        {loggedInUser && !isAdmin && (
          <>
            <section className="booking-section">
              <div className="section-heading">
                <h2>Book an Appointment</h2>
                <p>
                  Select an available date and time with our medical team.
                </p>
              </div>

              {loadingSlots ? (
                <p>Loading available appointments...</p>
              ) : slots.length === 0 ? (
                <div className="empty-state">
                  No appointment slots are currently available.
                </div>
              ) : (
                <form
                  className="booking-form"
                  onSubmit={handleBook}
                >
                  <label htmlFor="appointment-slot">
                    Available appointment
                  </label>

                  <select
                    id="appointment-slot"
                    value={selectedSlot}
                    onChange={(event) =>
                      setSelectedSlot(event.target.value)
                    }
                    required
                  >
                    <option value="">
                      Choose a doctor, date and time
                    </option>

                    {slots.map((slot) => (
                      <option key={slot.id} value={slot.id}>
                        {slot.doctor_name ||
                          getDoctorName(slot.doctor) ||
                          `Doctor #${slot.doctor}`}
                        {" · "}
                        {formatDate(slot.date)}
                        {" · "}
                        {formatTime(slot.start_time)}
                        {slot.end_time
                          ? `–${formatTime(slot.end_time)}`
                          : ""}
                      </option>
                    ))}
                  </select>

                  <label htmlFor="appointment-reason">
                    Reason for visit
                  </label>

                  <textarea
                    id="appointment-reason"
                    value={reason}
                    onChange={(event) =>
                      setReason(event.target.value)
                    }
                    placeholder="Briefly describe the reason for your visit"
                    rows="3"
                  />

                  <button type="submit" disabled={saving}>
                    {saving ? "Booking..." : "Book Appointment"}
                  </button>
                </form>
              )}
            </section>

            <section className="my-appointments">
              <div className="section-heading">
                <h2>My Appointments</h2>
                <p>View and manage your bookings.</p>
              </div>

              {appointments.length === 0 ? (
                <div className="empty-state">
                  You have no appointments yet. Book one above to get
                  started.
                </div>
              ) : (
                <div className="appointment-list">
                  {appointments.map((appointment, index) => {
                    const slot = getAppointmentSlot(appointment);
                    const status = String(
                      appointment.status || "confirmed"
                    ).toLowerCase();

                    const doctorName =
                      appointment.doctor_name ||
                      slot?.doctor_name ||
                      getDoctorName(slot?.doctor) ||
                      "";

                    const appointmentId =
                      getAppointmentId(appointment);

                    return (
                      <article
                        className="appointment-card"
                        key={appointmentId || index}
                      >
                        <div className="appointment-card-top">
                          <h3>
                            {doctorName || "Medical appointment"}
                          </h3>

                          <span
                            className={`appointment-status ${status}`}
                          >
                            {status}
                          </span>
                        </div>

                        <p>
                          <strong>Date:</strong>{" "}
                          {formatDate(
                            appointment.date || slot?.date
                          )}
                        </p>

                        <p>
                          <strong>Time:</strong>{" "}
                          {formatTime(
                            appointment.start_time ||
                              slot?.start_time
                          )}
                          {(appointment.end_time ||
                            slot?.end_time) &&
                            `–${formatTime(
                              appointment.end_time ||
                                slot?.end_time
                            )}`}
                        </p>

                        {appointment.reason && (
                          <p>
                            <strong>Reason:</strong>{" "}
                            {appointment.reason}
                          </p>
                        )}

                        {status === "confirmed" && (
                          <button
                            className="cancel-button"
                            onClick={() =>
                              handleCancel(appointmentId)
                            }
                            disabled={!appointmentId}
                          >
                            Cancel Appointment
                          </button>
                        )}
                      </article>
                    );
                  })}
                </div>
              )}
            </section>
          </>
        )}

        <section className="doctors-section">
          <div className="hero">
            <p>YOUR HEALTH, OUR PRIORITY</p>
            <h2>Meet our medical team</h2>
            <p>
              Find a doctor who understands your healthcare needs.
            </p>
          </div>

          <div className="section-heading">
            <h2>Our Doctors</h2>
            <p>Experienced professionals, here to help.</p>
          </div>

          {loadingDoctors && <p>Loading doctors...</p>}

          {!loadingDoctors &&
            doctors.length === 0 &&
            !error && <p>No doctors found.</p>}

          <div className="doctor-list">
            {doctors.map((doctor) => (
              <article
                className="doctor-card"
                key={doctor.id}
              >
                <div className="doctor-avatar">
                  {(doctor.first_name || "").charAt(0)}
                  {(doctor.last_name || "").charAt(0)}
                </div>

                <p className="doctor-specialisation">
                  {doctor.specialisation}
                </p>

                <h3>
                  Dr. {doctor.first_name} {doctor.last_name}
                </h3>

                <p>{doctor.bio}</p>

                <div className="doctor-contact">
                  <p>{doctor.email}</p>
                  <p>{doctor.phone}</p>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
