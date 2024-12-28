import axios from 'axios';

const API_URL = 'http://localhost:5246/api/Employees';

export const getEmployees = () => axios.get(API_URL).catch(error => console.error("Error fetching employees:", error));
export const getEmployeeById = (id) => axios.get(`${API_URL}/${id}`).catch(error => console.error("Error fetching employee by ID:", error));
export const addEmployee = (employee) => axios.post({ API_URL }, employee).catch(error => console.error("Error adding employee:", error));
export const updateEmployee = (id, employee) => axios.put(`${API_URL}/${id}`, employee).catch(error => console.error("Error updating employee:", error));
export const deleteEmployee = (id) => axios.delete(`${API_URL}/${id}`).catch(error => console.error("Error deleting employee:", error));
