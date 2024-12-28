import React, { useState } from 'react';
import EmployeeList from './EmployeeList';
import EmployeeForm from './EmployeeForm';

function App() {
  const [selectedEmployee, setSelectedEmployee] = useState(null);

  const handleEdit = (employee) => {
    setSelectedEmployee(employee);
  };

  const handleSave = () => {
    setSelectedEmployee(null);
  };

  return (
    <div>
      <h1>Employee Management</h1>
      <EmployeeForm selectedEmployee={selectedEmployee} onSave={handleSave} />
      <EmployeeList onEdit={handleEdit} />
    </div>
  );
}

export default App;
