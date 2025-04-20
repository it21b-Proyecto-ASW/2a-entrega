// API Configuration
const API_BASE_URL = '/api/v1';

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    try {
        const token = await firebase.auth().currentUser?.getIdToken();
        if (!token) {
            throw new Error('No authentication token available');
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

// API Implementation for Issue Tracker
const API = {
    // Helper function for making HTTP requests
    async request(method, endpoint, data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${await this.getAuthToken()}`
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`/api${endpoint}`, options);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Error en la petició');
            }

            return await response.json();
        } catch (error) {
            console.error(`Error en la petició ${method} ${endpoint}:`, error);
            throw error;
        }
    },

    // Get authentication token
    async getAuthToken() {
        const user = firebase.auth().currentUser;
        if (!user) {
            throw new Error('No hi ha usuari autenticat');
        }
        return await user.getIdToken();
    },

    // Issues endpoints
    issues: {
        // List all issues with optional filters
        async list(filters = {}) {
            const queryParams = new URLSearchParams();
            Object.entries(filters).forEach(([key, value]) => {
                if (value) queryParams.append(key, value);
            });
            
            const endpoint = `/issues${queryParams.toString() ? `?${queryParams}` : ''}`;
            return await API.request('GET', endpoint);
        },

        // Get a single issue
        async get(id) {
            return await API.request('GET', `/issues/${id}`);
        },

        // Create a new issue
        async create(issueData) {
            return await API.request('POST', '/issues', issueData);
        },

        // Update an issue
        async update(id, issueData) {
            return await API.request('PUT', `/issues/${id}`, issueData);
        },

        // Delete an issue
        async delete(id) {
            return await API.request('DELETE', `/issues/${id}`);
        }
    },

    // Comments endpoints
    comments: {
        // List comments for an issue
        async list(issueId) {
            return await API.request('GET', `/issues/${issueId}/comments`);
        },

        // Add a comment to an issue
        async add(issueId, commentData) {
            return await API.request('POST', `/issues/${issueId}/comments`, commentData);
        }
    },

    // Attachments endpoints
    attachments: {
        // List attachments for an issue
        async list(issueId) {
            return await API.request('GET', `/issues/${issueId}/attachments`);
        },

        // Add an attachment to an issue
        async add(issueId, file) {
            const formData = new FormData();
            formData.append('file', file);

            const options = {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${await API.getAuthToken()}`
                },
                body: formData
            };

            const response = await fetch(`/api/issues/${issueId}/attachments`, options);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Error pujant l\'arxiu');
            }

            return await response.json();
        },

        // Delete an attachment
        async delete(issueId, attachmentId) {
            return await API.request('DELETE', `/issues/${issueId}/attachments/${attachmentId}`);
        }
    },

    // Users endpoints
    users: {
        // Get user profile
        async get(id) {
            return await API.request('GET', `/users/${id}`);
        },

        // Update user profile
        async update(id, userData) {
            return await API.request('PUT', `/users/${id}`, userData);
        },

        // Get user's issues
        async getIssues(id) {
            return await API.request('GET', `/users/${id}/issues`);
        },

        // Get user's comments
        async getComments(id) {
            return await API.request('GET', `/users/${id}/comments`);
        }
    }
};

// Export API modules
window.API = API; 