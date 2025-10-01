const BASE = "http://localhost:5000/api/";

export default function autofetch(url, options = {}) {
    const { method = 'GET', headers = {}, body } = options;

    const response = fetch(BASE + url, {
        method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            ...headers,
        },
        body: body ? body : undefined,
    });

    return response.then((res) => {
        if (!res.ok) {
            return res.json().then((errorData) => {
                throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
            });
        }
        return res.json();
    })
        .then((json) => {
            return json;
        })
        .catch((error) => {
            console.error('Fetch error:', error);
            throw error;
        });
}