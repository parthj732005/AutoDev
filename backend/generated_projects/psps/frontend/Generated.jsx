Here’s a simple functional React component that allows users to authenticate using their email and password. The component is styled with Tailwind CSS classes and does not rely on any external libraries:

```jsx
import React, { useState } from 'react';

const AuthComponent = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add authentication logic here

        // Example validation
        if (!email || !password) {
            setErrorMessage('Email and password are required');
            return;
        }
        
        // Dummy authentication logic for demonstration
        if (email === 'test@example.com' && password === 'password123') {
            alert('Authentication successful!');
            setErrorMessage('');
        } else {
            setErrorMessage('Invalid email or password');
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="bg-white p-6 rounded shadow-md w-80">
                <h2 className="text-center text-2xl font-bold mb-4">Login</h2>
                {errorMessage && <div className="bg-red-200 text-red-600 p-2 rounded mb-4">{errorMessage}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-gray-700 mb-2" htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full border border-gray-300 p-2 rounded"
                            placeholder="Enter your email"
                            required
                        />
