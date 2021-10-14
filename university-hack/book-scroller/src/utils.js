const getCookie = (name) => {
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
};

export const getParents = (node, parents = [node]) => {
    try {
        const parent = node.parentNode;
        if (parent) {
            return getParents(node.parentNode, [...parents, parent])
        } else {
            return parents
        }
    } catch (e) {
        return []
    }
};

export function apiRequest (
    func,
    apiMethod,
    {
        data = false,
        method = "GET",
    } = {}
) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const response = JSON.parse(this.responseText);
            func(response)
        }
    };
    const {protocol, host, hostname} = window.location;
    if (protocol === 'http:') {
        xhttp.open(method, `${protocol}//${hostname}:8000/api/${apiMethod}/`, true);
    } else {
        xhttp.open(method, `${protocol}//${host}/api/${apiMethod}/`, true);
    }
    if (data) {
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhttp.send(JSON.stringify(data));
    } else {
        xhttp.send()
    }
}
