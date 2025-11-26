import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import SubmitClaim from './components/SubmitClaim';
import ClaimsList from './components/ClaimsList';
import ClaimDetails from './components/ClaimDetails';
import Toast from './components/Toast';

function Navigation() {
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    return (
        <nav style={{
            background: 'var(--color-white)',
            boxShadow: 'var(--shadow-md)',
            position: 'sticky',
            top: 0,
            zIndex: 100,
        }}>
            <div className="container" style={{ padding: 'var(--spacing-lg)' }}>
                <div className="flex items-center justify-between">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            background: 'linear-gradient(135deg, var(--color-red-primary), var(--color-red-dark))',
                            borderRadius: 'var(--radius-md)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            fontWeight: 'bold',
                            fontSize: 'var(--font-size-xl)',
                            boxShadow: 'var(--shadow-glossy)',
                        }}>
                            +
                        </div>
                        <h1 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 600, margin: 0 }}>
                            OPD Claim System
                        </h1>
                    </div>

                    <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
                        <Link
                            to="/"
                            style={{
                                padding: 'var(--spacing-sm) var(--spacing-lg)',
                                borderRadius: 'var(--radius-md)',
                                textDecoration: 'none',
                                fontWeight: 500,
                                transition: 'all var(--transition-normal)',
                                ...(isActive('/') ? {
                                    background: 'linear-gradient(135deg, var(--color-red-primary), var(--color-red-dark))',
                                    color: 'var(--color-white)',
                                    boxShadow: 'var(--shadow-glossy)',
                                } : {
                                    color: 'var(--color-red-primary)',
                                    background: 'transparent',
                                }),
                            }}
                            onMouseEnter={(e) => {
                                if (!isActive('/')) {
                                    e.currentTarget.style.background = 'var(--color-cream)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (!isActive('/')) {
                                    e.currentTarget.style.background = 'transparent';
                                }
                            }}
                        >
                            Submit Claim
                        </Link>
                        <Link
                            to="/claims"
                            style={{
                                padding: 'var(--spacing-sm) var(--spacing-lg)',
                                borderRadius: 'var(--radius-md)',
                                textDecoration: 'none',
                                fontWeight: 500,
                                transition: 'all var(--transition-normal)',
                                ...(isActive('/claims') ? {
                                    background: 'linear-gradient(135deg, var(--color-red-primary), var(--color-red-dark))',
                                    color: 'var(--color-white)',
                                    boxShadow: 'var(--shadow-glossy)',
                                } : {
                                    color: 'var(--color-red-primary)',
                                    background: 'transparent',
                                }),
                            }}
                            onMouseEnter={(e) => {
                                if (!isActive('/claims')) {
                                    e.currentTarget.style.background = 'var(--color-cream)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (!isActive('/claims')) {
                                    e.currentTarget.style.background = 'transparent';
                                }
                            }}
                        >
                            View Claims
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

export interface ToastMessage {
    id: number;
    type: 'success' | 'error' | 'info';
    message: string;
}

function App() {
    const [toasts, setToasts] = useState<ToastMessage[]>([]);

    const showToast = (type: 'success' | 'error' | 'info', message: string) => {
        const id = Date.now();
        setToasts(prev => [...prev, { id, type, message }]);
    };

    const removeToast = (id: number) => {
        setToasts(prev => prev.filter(toast => toast.id !== id));
    };

    return (
        <Router>
            <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navigation />

                <main style={{ flex: 1, padding: 'var(--spacing-2xl) 0' }}>
                    <Routes>
                        <Route path="/" element={<SubmitClaim showToast={showToast} />} />
                        <Route path="/claims" element={<ClaimsList />} />
                        <Route path="/claims/:claimId" element={<ClaimDetails />} />
                    </Routes>
                </main>

                <footer style={{
                    background: 'var(--color-white)',
                    borderTop: '1px solid var(--color-gray-light)',
                    padding: 'var(--spacing-lg)',
                    textAlign: 'center',
                    color: 'var(--color-gray)',
                    fontSize: 'var(--font-size-sm)',
                }}>
                    © 2024 OPD Claim Adjudication System. Powered by AI.
                </footer>

                {toasts.map(toast => (
                    <Toast
                        key={toast.id}
                        type={toast.type}
                        message={toast.message}
                        onClose={() => removeToast(toast.id)}
                    />
                ))}
            </div>
        </Router>
    );
}

export default App;
