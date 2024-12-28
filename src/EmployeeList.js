import React, { useEffect, useState } from 'react';
import { getEmployees, deleteEmployee } from './EmployeeService';

function EmployeeList({ onEdit }) {
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        const response = await getEmployees();
        setEmployees(response.data);
    };

    const handleDelete = async (id) => {
        await deleteEmployee(id);
        fetchEmployees();
    };

    return (
        <div>
            <h2>Employee List</h2>
            <ul>
                {employees.map(employee => (
                    <li key={employee.id}>
                        {employee.name} - {employee.department} - ${employee.salary}
                        <button onClick={() => onEdit(employee)}>Edit</button>
                        <button onClick={() => handleDelete(employee.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EmployeeList;
