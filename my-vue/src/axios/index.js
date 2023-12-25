import axios from 'axios'

const instance = axios.create({
    timeout: 10000,
    baseURL: process.env.NODE_ENV === 'production' ? '/api' : '/',
    headers: {
        'Content-Type': 'application/json;charset=UTF-8;',
    },
    withCredentials: true
})

export default instance;