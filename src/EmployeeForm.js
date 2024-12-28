import React, { useState, useEffect } from 'react';
import { addEmployee, updateEmployee } from './EmployeeService';

function EmployeeForm({ selectedEmployee, onSave }) {
    const [employee, setEmployee] = useState({ id: '', name: '', department: '', salary: '' });

    useEffect(() => {
        if (selectedEmployee) {
            setEmployee(selectedEmployee);
        }
    }, [selectedEmployee]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEmployee({ ...employee, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (employee.id) {
            await updateEmployee(employee.id, employee);
        } else {
            await addEmployee(employee);
        }
        onSave();
        setEmployee({ id: '', name: '', department: '', salary: '' });
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>{employee.id ? 'Edit' : 'Add'} Employee</h2>
            <input name="name" value={employee.name} onChange={handleChange} placeholder="Name" required />
            <input name="department" value={employee.department} onChange={handleChange} placeholder="Department" required />
            <input name="salary" type="number" value={employee.salary} onChange={handleChange} placeholder="Salary" required />
            <button type="submit">{employee.id ? 'Update' : 'Add'} Employee</button>
        </form>
    );
}

export default EmployeeForm;
