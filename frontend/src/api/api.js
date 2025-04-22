import axios from "axios";

export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getUsers = async () => {
    try {
        const response = await api.get(`${window._env_.VITE_APP_API_URL}/users`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};

export const createUser = async (user) => {
    try {
        const response = await api.post(`${window._env_.VITE_APP_API_URL}/users`, user);
        return response.data;
    } catch (error) {
        console.error("Error creating user:", error);
        throw error;
    }
}

export const deleteUser = async (id) => {
    try {
        await api.delete(`${window._env_.VITE_APP_API_URL}/users/${id}`);

    } catch (error) {
        console.error("Error deleting user:", error);
        throw error;
    }
}

export const editUser = async (id, user) => {
    try {
        await api.put(`${window._env_.VITE_APP_API_URL}/users/${id}`, user);
    } catch (error) {
        console.error("Error edit user:", error);
        throw error;
    }
}