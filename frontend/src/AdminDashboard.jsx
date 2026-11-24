import { useCallback, useEffect, useState } from "react";
import api from "./api";
import "./AdminDashboard.css";

function AdminDashboard({ onLogout }) {
  const [section, setSection] = useState("overview");
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [doctorForm, setDoctorForm] = useState({
    first_name: "", last_name: "", specialisation: "", email: "",
    phone: "", bio: ""
  });

  const [slotForm, setSlotForm] = useState({
    doctor: "", date: "", start_time: "", end_time: ""
  });

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [a, d, s] = await Promise.all([
        api.get("/api/admin/appointments/"),
        api.get("/api/admin/doctors/"),
        api.get("/api/admin/slots/")
      ]);
      setAppointments(Array.isArray(a.data) ? a.data : a.data.results || []);
      setDoctors(Array.isArray(d.data) ? d.data : d.data.results || []);
      setSlots(Array.isArray(s.data) ? s.data : s.data.results || []);
    } catch (err) {
      setError(
        err.response?.status === 403
          ? "Access denied. Sign in with a staff administrator account."
          : err.response?.data?.detail || "Could not load dashboard data."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  async function addDoctor(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api.post("/api/admin/doctors/", doctorForm);
      setDoctorForm({
        first_name: "", last_name: "", specialisation: "", email: "",
        phone: "", bio: ""
      });
      setMessage("Doctor added successfully.");
      await loadData();
    } catch (err) {
      setError(err.response?.data?.error || "Could not add doctor.");
    }
  }

  async function addSlot(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api.post("/api/admin/slots/", {
        ...slotForm,
        doctor: Number(slotForm.doctor)
      });
      setSlotForm({
        doctor: "", date: "", start_time: "", end_time: ""
      });
      setMessage("Appointment slot added successfully.");
      await loadData();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Could not add slot. Check the details and try again."
      );
    }
  }

  function appointmentPatient(item) {
    return item.patient_name || item.patient_username ||
      item.patient?.username || "Patient";
  }

  function appointmentDoctor(item) {
    return item.doctor_name ||
      item.slot_details?.doctor_name ||
      item.slot?.doctor_name ||
      item.slot?.doctor?.first_name ||
      "Doctor";
  }

  function appointmentDate(item) {
    const slot = item.slot_details || item.slot || {};
    return slot.date || item.date || "—";
  }

  function appointmentTime(item) {
    const slot = item.slot_details || item.slot || {};
    return slot.start_time || item.start_time || "—";
  }

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <h2>Piki Ora</h2>
        <p className="admin-label">ADMINISTRATION</p>
        {[
          ["overview", "Overview"],
          ["appointments", "Appointments"],
          ["doctors", "Doctors"],
          ["slots", "Appointment Slots"]
        ].map(([key, label]) => (
          <button
            key={key}
            className={section === key ? "admin-nav active" : "admin-nav"}
            onClick={() => setSection(key)}
          >
            {label}
          </button>
        ))}
        <button className="admin-nav admin-logout" onClick={onLogout}>
          Log Out
        </button>
      </aside>

      <main className="admin-main">
        <header className="admin-header">
          <div>
            <h1>
              {section === "overview" ? "Dashboard Overview" :
               section === "appointments" ? "Appointments" :
               section === "doctors" ? "Manage Doctors" :
               "Manage Appointment Slots"}
            </h1>
            <p>Manage Piki Ora Medical Centre.</p>
          </div>
          <button className="admin-refresh" onClick={loadData}>
            Refresh Data
          </button>
        </header>

        {error && <p className="admin-alert error">{error}</p>}
        {message && <p className="admin-alert success">{message}</p>}
        {loading && <p>Loading dashboard...</p>}

        {!loading && section === "overview" && (
          <>
            <div className="admin-stats">
              <article className="admin-stat">
                <span>Total Appointments</span>
                <strong>{appointments.length}</strong>
              </article>
              <article className="admin-stat">
                <span>Total Doctors</span>
                <strong>{doctors.length}</strong>
              </article>
              <article className="admin-stat">
                <span>Appointment Slots</span>
                <strong>{slots.length}</strong>
              </article>
              <article className="admin-stat">
                <span>Confirmed Appointments</span>
                <strong>{appointments.filter(a => a.status === "confirmed").length}</strong>
              </article>
            </div>

            <section className="admin-panel">
              <h2>Recent Appointments</h2>
              {appointments.length === 0 ? (
                <p>No appointments found.</p>
              ) : (
                <div className="admin-table-wrap">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>Patient</th><th>Doctor</th><th>Date</th>
                        <th>Time</th><th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {appointments.slice(0, 5).map((a, index) => (
                        <tr key={a.id || index}>
                          <td>{appointmentPatient(a)}</td>
                          <td>{appointmentDoctor(a)}</td>
                          <td>{appointmentDate(a)}</td>
                          <td>{appointmentTime(a)}</td>
                          <td>{a.status || "—"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          </>
        )}

        {!loading && section === "appointments" && (
          <section className="admin-panel">
            <h2>All Appointments</h2>
            {appointments.length === 0 ? <p>No appointments found.</p> : (
              <div className="admin-table-wrap">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>Patient</th><th>Doctor</th><th>Date</th>
                      <th>Time</th><th>Status</th><th>Reason</th>
                    </tr>
                  </thead>
                  <tbody>
                    {appointments.map((a, index) => (
                      <tr key={a.id || index}>
                        <td>{appointmentPatient(a)}</td>
                        <td>{appointmentDoctor(a)}</td>
                        <td>{appointmentDate(a)}</td>
                        <td>{appointmentTime(a)}</td>
                        <td>{a.status || "—"}</td>
                        <td>{a.reason || "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        )}

        {!loading && section === "doctors" && (
          <div className="admin-columns">
            <section className="admin-panel">
              <h2>Add Doctor</h2>
              <form className="admin-form" onSubmit={addDoctor}>
                <label>First Name<input required value={doctorForm.first_name}
                  onChange={e => setDoctorForm({...doctorForm, first_name:e.target.value})}/></label>
                <label>Last Name<input required value={doctorForm.last_name}
                  onChange={e => setDoctorForm({...doctorForm, last_name:e.target.value})}/></label>
                <label>Specialisation<input required value={doctorForm.specialisation}
                  onChange={e => setDoctorForm({...doctorForm, specialisation:e.target.value})}/></label>
                <label>Email<input required type="email" value={doctorForm.email}
                  onChange={e => setDoctorForm({...doctorForm, email:e.target.value})}/></label>
                <label>Phone<input value={doctorForm.phone}
                  onChange={e => setDoctorForm({...doctorForm, phone:e.target.value})}/></label>
                <label>Bio<textarea value={doctorForm.bio}
                  onChange={e => setDoctorForm({...doctorForm, bio:e.target.value})}/></label>
                <button type="submit">Add Doctor</button>
              </form>
            </section>
            <section className="admin-panel">
              <h2>Doctors ({doctors.length})</h2>
              {doctors.map(d => (
                <article className="admin-list-item" key={d.id}>
                  <strong>Dr. {d.first_name} {d.last_name}</strong>
                  <p>{d.specialisation}</p>
                  <small>{d.email}</small>
                </article>
              ))}
            </section>
          </div>
        )}

        {!loading && section === "slots" && (
          <div className="admin-columns">
            <section className="admin-panel">
              <h2>Create Appointment Slot</h2>
              <form className="admin-form" onSubmit={addSlot}>
                <label>Doctor
                  <select required value={slotForm.doctor}
                    onChange={e => setSlotForm({...slotForm, doctor:e.target.value})}>
                    <option value="">Select doctor</option>
                    {doctors.map(d => (
                      <option key={d.id} value={d.id}>
                        Dr. {d.first_name} {d.last_name}
                      </option>
                    ))}
                  </select>
                </label>
                <label>Date<input type="date" required min={new Date().toISOString().slice(0,10)}
                  value={slotForm.date}
                  onChange={e => setSlotForm({...slotForm, date:e.target.value})}/></label>
                <label>Start Time<input type="time" required value={slotForm.start_time}
                  onChange={e => setSlotForm({...slotForm, start_time:e.target.value})}/></label>
                <label>End Time<input type="time" required value={slotForm.end_time}
                  onChange={e => setSlotForm({...slotForm, end_time:e.target.value})}/></label>
                <button type="submit">Create Slot</button>
              </form>
            </section>
            <section className="admin-panel">
              <h2>Available Slots ({slots.length})</h2>
              {slots.map((slot, index) => (
                <article className="admin-list-item" key={slot.id || index}>
                  <strong>{slot.doctor_name || slot.doctor?.name || `Doctor #${slot.doctor}`}</strong>
                  <p>{slot.date} · {slot.start_time}–{slot.end_time}</p>
                </article>
              ))}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

export default AdminDashboard;
