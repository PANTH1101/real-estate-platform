// API utility for JWT-based authentication and API calls
const API_BASE = '/api';

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make API request with credentials
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const csrftoken = getCookie('csrftoken');
    
    const defaultOptions = {
        credentials: 'include', // Include cookies (JWT)
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (csrftoken) {
        defaultOptions.headers['X-CSRFToken'] = csrftoken;
    }
    
    if (options.method && options.method !== 'GET' && options.method !== 'HEAD') {
        defaultOptions.headers['X-CSRFToken'] = csrftoken || '';
    }
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json().catch(() => ({}));
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Auth API
const authAPI = {
    register: (data) => apiRequest('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    login: (data) => apiRequest('/auth/login/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    logout: () => apiRequest('/auth/logout/', { method: 'POST' }),
    refresh: () => apiRequest('/auth/refresh/', { method: 'POST' }),
    getProfile: () => apiRequest('/users/profile/'),
    updateProfile: (data) => apiRequest('/users/profile/', {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
};

// Property API
const propertyAPI = {
    list: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/properties/${query ? '?' + query : ''}`);
    },
    search: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/properties/search/${query ? '?' + query : ''}`);
    },
    get: (id) => apiRequest(`/properties/${id}/`),
    create: (data) => apiRequest('/properties/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    update: (id, data) => apiRequest(`/properties/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    delete: (id) => apiRequest(`/properties/${id}/`, { method: 'DELETE' }),
};

// Wishlist API
const wishlistAPI = {
    list: () => apiRequest('/wishlist/'),
    add: (propertyId) => apiRequest('/wishlist/add/', {
        method: 'POST',
        body: JSON.stringify({ property_id: propertyId }),
    }),
    remove: (propertyId) => apiRequest(`/wishlist/remove/${propertyId}/`, {
        method: 'DELETE',
    }),
};

// Enquiry API
const enquiryAPI = {
    create: (data) => apiRequest('/enquiries/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    listSeller: () => apiRequest('/enquiries/seller/'),
};

// Admin API
const adminAPI = {
    getUsers: () => apiRequest('/admin/users/'),
    approveProperty: (id) => apiRequest(`/admin/property/${id}/approve/`, {
        method: 'PUT',
    }),
    getAnalytics: () => apiRequest('/admin/analytics/'),
};

// Check if user is authenticated
async function checkAuth() {
    try {
        const profile = await authAPI.getProfile();
        return profile;
    } catch {
        return null;
    }
}

// Redirect if not authenticated
async function requireAuth(redirectTo = '/accounts/login/') {
    const user = await checkAuth();
    if (!user) {
        window.location.href = redirectTo;
        return null;
    }
    return user;
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0,
    }).format(amount);
}

// Show alert/toast
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    setTimeout(() => alertDiv.remove(), 5000);
}

