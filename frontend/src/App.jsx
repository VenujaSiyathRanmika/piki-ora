
import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://localhost:8000";

axios.defaults.withCredentials = true;

function App() {
  const [doctors, setDoctors] = useState([]);
  const [slots, setSlots] = useState([]);
  const [appointments, setAppointments] = useState([]);

  const [page, setPage] = useState("home");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginType, setLoginType] = useState("patient");
  const [loggedIn, setLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  const [selectedSlot, setSelectedSlot] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");

  const emptyDoctor = {
    first_name: "",
    last_name: "",
    specialisation: "",
    email: "",
    phone: "",
    bio: "",
  };

  const [doctorForm, setDoctorForm] = useState(emptyDoctor);
  const [editingDoctorId, setEditingDoctorId] = useState(null);

  useEffect(() => {
    loadDoctors();
    loadSlots();
  }, []);

  // Postman 1: Get CSRF token
  async function getCsrfToken() {
    const response = await axios.get(
      `${API}/accounts/api/csrf/`
    );

    return response.data.csrfToken;
  }

  // Get doctors
  async function loadDoctors() {
    try {
      const response = await axios.get(
        `${API}/api/doctors/`
      );

      setDoctors(
        Array.isArray(response.data) ? response.data : []
      );
    } catch (error) {
      console.error("Load doctors:", error);
      setMessage("Could not load doctors.");
    }
  }

  // Postman 4: Get appointment slots
  async function loadSlots() {
    try {
      const response = await axios.get(
        `${API}/appointments/api/slots/`
      );

      setSlots(
        Array.isArray(response.data) ? response.data : []
      );
    } catch (error) {
      console.error("Load slots:", error);
      setMessage("Could not load appointment slots.");
    }
  }

  function openLogin(type) {
    setLoginType(type);
    setPage("login");
    setMessage("");
  }

  // Postman 2 and 3: Patient/Admin login
  async function handleLogin(event) {
    event.preventDefault();
    setMessage("Logging in...");

    try {
      const csrfToken = await getCsrfToken();

      const response = await axios.post(
        `${API}/accounts/api/login/`,
        {
          username,
          password,
          loginType,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        }
      );

      const data = response.data;

      setLoggedIn(true);
      setIsAdmin(Boolean(data.is_admin));
      setPassword("");
      setMessage("Login successful.");

      if (data.is_admin) {
        setPage("admin");
        await loadDoctors();
        await loadSlots();
      } else {
        setPage("dashboard");
        await loadAppointments();
      }
    } catch (error) {
      console.error("Login:", error);

      setMessage(
        error.response?.data?.error ||
          "Login failed. Check your username and password."
      );
    }
  }

  // Postman 5: Get appointments
  async function loadAppointments() {
    try {
      const response = await axios.get(
        `${API}/appointments/api/`
      );

      setAppointments(
        Array.isArray(response.data) ? response.data : []
      );
    } catch (error) {
      console.error("Load appointments:", error);

      setMessage(
        error.response?.data?.error ||
          "Could not load appointments."
      );
    }
  }

  // Postman 6: Book appointment
  async function bookAppointment(event) {
    event.preventDefault();

    if (!loggedIn || isAdmin) {
      setMessage("Please log in as a patient first.");
      return;
    }

    try {
      const csrfToken = await getCsrfToken();

      await axios.post(
        `${API}/appointments/api/`,
        {
          slot: Number(selectedSlot),
          reason,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setMessage("Appointment booked successfully.");
      setSelectedSlot("");
      setReason("");

      await loadAppointments();
      setPage("dashboard");
    } catch (error) {
      console.error("Book appointment:", error);

      const data = error.response?.data;

      setMessage(
        data?.error ||
          data?.slot?.[0] ||
          (data ? JSON.stringify(data) : "Booking failed.")
      );
    }
  }

  // Postman 7: Cancel appointment
  async function cancelAppointment(id) {
    if (
      !window.confirm(
        "Do you want to cancel this appointment?"
      )
    ) {
      return;
    }

    try {
      const csrfToken = await getCsrfToken();

      await axios.post(
        `${API}/appointments/api/${id}/cancel/`,
        {},
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setMessage("Appointment cancelled successfully.");
      await loadAppointments();
    } catch (error) {
      console.error("Cancel appointment:", error);

      setMessage(
        error.response?.data?.error ||
          "Could not cancel appointment."
      );
    }
  }

  function updateDoctorField(event) {
    const { name, value } = event.target;

    setDoctorForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  function startEditDoctor(doctor) {
    setEditingDoctorId(doctor.id);

    setDoctorForm({
      first_name: doctor.first_name || "",
      last_name: doctor.last_name || "",
      specialisation: doctor.specialisation || "",
      email: doctor.email || "",
      phone: doctor.phone || "",
      bio: doctor.bio || "",
    });

    setMessage(
      `Editing Dr. ${doctor.first_name} ${doctor.last_name}.`
    );

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  function resetDoctorForm() {
    setEditingDoctorId(null);
    setDoctorForm({ ...emptyDoctor });
  }

  // Postman 8: Add doctor
  // Postman 9: Edit doctor
  async function saveDoctor(event) {
    event.preventDefault();

    try {
      const csrfToken = await getCsrfToken();

      if (editingDoctorId !== null) {
        await axios.put(
          `${API}/api/doctors/${editingDoctorId}/edit/`,
          doctorForm,
          {
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
          }
        );

        setMessage("Doctor updated successfully.");
      } else {
        await axios.post(
          `${API}/api/doctors/add/`,
          doctorForm,
          {
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
          }
        );

        setMessage("Doctor added successfully.");
      }

      resetDoctorForm();

      await loadDoctors();
      await loadSlots();
    } catch (error) {
      console.error("Save doctor:", error);

      const data = error.response?.data;

      setMessage(
        data?.error ||
          (data ? JSON.stringify(data) : "Could not save doctor.")
      );
    }
  }

  // Postman 10: Delete doctor
  async function deleteDoctor(id) {
    if (
      !window.confirm(
        "Are you sure you want to delete this doctor?"
      )
    ) {
      return;
    }

    try {
      const csrfToken = await getCsrfToken();

      await axios.delete(
        `${API}/api/doctors/${id}/delete/`,
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setMessage("Doctor deleted successfully.");

      if (editingDoctorId === id) {
        resetDoctorForm();
      }

      await loadDoctors();
      await loadSlots();
    } catch (error) {
      console.error("Delete doctor:", error);

      setMessage(
        error.response?.data?.error ||
          "Could not delete doctor."
      );
    }
  }

  // Logout using Django session authentication
  async function handleLogout() {
    try {
      const csrfToken = await getCsrfToken();

      await axios.post(
        `${API}/accounts/api/logout/`,
        {},
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setLoggedIn(false);
      setIsAdmin(false);
      setUsername("");
      setPassword("");
      setAppointments([]);
      setPage("home");
      setMessage("Logged out successfully.");
    } catch (error) {
      console.error("Logout:", error);

      setMessage(
        error.response?.data?.error ||
          "Could not log out."
      );
    }
  }

  return (
    <div>
      <h1>Piki Ora Medical Centre</h1>

      <nav className="navigation">
        <button onClick={() => setPage("home")}>
          Home
        </button>

        {!loggedIn && (
          <>
            <button onClick={() => openLogin("patient")}>
              Patient Login
            </button>

            <button onClick={() => openLogin("admin")}>
              Admin Login
            </button>

            <a href={`${API}/accounts/register/`}>
              Register
            </a>
          </>
        )}

        {loggedIn && (
          <>
            <button
              onClick={() => {
                if (isAdmin) {
                  setPage("admin");
                } else {
                  setPage("dashboard");
                  loadAppointments();
                }
              }}
            >
              Dashboard
            </button>

            <button onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </nav>

      <p>{message}</p>

      {page === "login" && (
        <div className="login-form">
          <h2>
            {loginType === "patient"
              ? "Patient Login"
              : "Administrator Login"}
          </h2>

          <form onSubmit={handleLogin}>
            <label>Username</label>

            <input
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              required
            />

            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

            <button type="submit">
              Login
            </button>
          </form>
        </div>
      )}

      {page === "home" && (
        <>
          <h2>Our Doctors</h2>

          {doctors.map((doctor) => (
            <div className="doctor" key={doctor.id}>
              <h3>
                Dr. {doctor.first_name} {doctor.last_name}
              </h3>

              <p>{doctor.specialisation}</p>
              <p>{doctor.bio}</p>
            </div>
          ))}

          <h2>Appointment Slots</h2>

          {slots.map((slot) => (
            <div className="doctor" key={slot.id}>
              <p>{slot.doctor_name}</p>
              <p>{slot.date}</p>

              <p>
                {slot.start_time} - {slot.end_time}
              </p>
            </div>
          ))}

          <h2>Book an Appointment</h2>

          {!loggedIn && (
            <p>
              Please log in as a patient before booking.
            </p>
          )}

          <form
            className="booking-form"
            onSubmit={bookAppointment}
          >
            <label>Select a slot</label>

            <select
              value={selectedSlot}
              onChange={(event) =>
                setSelectedSlot(event.target.value)
              }
              required
              disabled={!loggedIn || isAdmin}
            >
              <option value="">Choose a slot</option>

              {slots.map((slot) => (
                <option key={slot.id} value={slot.id}>
                  {slot.doctor_name} - {slot.date} -{" "}
                  {slot.start_time}
                </option>
              ))}
            </select>

            <label>Reason for appointment</label>

            <textarea
              value={reason}
              onChange={(event) =>
                setReason(event.target.value)
              }
              required
              disabled={!loggedIn || isAdmin}
            />

            <button
              type="submit"
              disabled={!loggedIn || isAdmin}
            >
              Book Appointment
            </button>
          </form>
        </>
      )}

      {page === "dashboard" &&
        loggedIn &&
        !isAdmin && (
          <div>
            <h2>My Appointments</h2>

            <p>Welcome, {username}.</p>

            <button onClick={loadAppointments}>
              Refresh Appointments
            </button>

            {appointments.length === 0 && (
              <p>You have no appointments yet.</p>
            )}

            {appointments.map((appointment) => (
              <div
                className="doctor"
                key={appointment.id}
              >
                <h3>
                  Appointment #{appointment.id}
                </h3>

                <p>Reason: {appointment.reason}</p>
                <p>Status: {appointment.status}</p>

                <p>
                  Slot:{" "}
                  {typeof appointment.slot === "object"
                    ? `${appointment.slot?.date || ""} ${
                        appointment.slot?.start_time || ""
                      }`
                    : appointment.slot}
                </p>

                {appointment.status === "confirmed" && (
                  <button
                    onClick={() =>
                      cancelAppointment(appointment.id)
                    }
                  >
                    Cancel Appointment
                  </button>
                )}
              </div>
            ))}

            <button onClick={() => setPage("home")}>
              Book Another Appointment
            </button>
          </div>
        )}

      {page === "admin" &&
        loggedIn &&
        isAdmin && (
          <div>
            <h2>Administrator Dashboard</h2>

            <p>Welcome, {username}.</p>
            <p>You are logged in as an administrator.</p>

            <h3>
              {editingDoctorId !== null
                ? "Edit Doctor"
                : "Add Doctor"}
            </h3>

            <form
              className="booking-form"
              onSubmit={saveDoctor}
            >
              <label>First Name</label>

              <input
                name="first_name"
                value={doctorForm.first_name}
                onChange={updateDoctorField}
                required
              />

              <label>Last Name</label>

              <input
                name="last_name"
                value={doctorForm.last_name}
                onChange={updateDoctorField}
                required
              />

              <label>Specialisation</label>

              <input
                name="specialisation"
                value={doctorForm.specialisation}
                onChange={updateDoctorField}
                required
              />

              <label>Email</label>

              <input
                type="email"
                name="email"
                value={doctorForm.email}
                onChange={updateDoctorField}
              />

              <label>Phone</label>

              <input
                name="phone"
                value={doctorForm.phone}
                onChange={updateDoctorField}
              />

              <label>Biography</label>

              <textarea
                name="bio"
                value={doctorForm.bio}
                onChange={updateDoctorField}
              />

              <button type="submit">
                {editingDoctorId !== null
                  ? "Save Changes"
                  : "Add Doctor"}
              </button>

              {editingDoctorId !== null && (
                <button
                  type="button"
                  onClick={resetDoctorForm}
                >
                  Cancel Edit
                </button>
              )}
            </form>

            <h3>Manage Doctors</h3>

            {doctors.map((doctor) => (
              <div className="doctor" key={doctor.id}>
                <p>
                  Dr. {doctor.first_name} {doctor.last_name}
                </p>

                <p>{doctor.specialisation}</p>

                <button
                  onClick={() => startEditDoctor(doctor)}
                >
                  Edit Doctor
                </button>

                <button
                  onClick={() => deleteDoctor(doctor.id)}
                >
                  Delete Doctor
                </button>
              </div>
            ))}

            <h3>Manage Patients</h3>

            <p>
              View registered patients, edit their details,
              and activate or deactivate patient accounts.
            </p>

            <a
              href={`${API}/dashboard/admin/patients/`}
              target="_blank"
              rel="noreferrer"
            >
              Manage Patients / Edit Patient
            </a>

            <h3>Available Appointment Slots</h3>

            {slots.map((slot) => (
              <div className="doctor" key={slot.id}>
                <p>{slot.doctor_name}</p>
                <p>{slot.date}</p>

                <p>
                  {slot.start_time} - {slot.end_time}
                </p>
              </div>
            ))}
          </div>
        )}
    </div>
  );
}

export default App;
