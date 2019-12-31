export const getInitialUrlForRequests = () => {
    const { protocol, hostname, port } = window.location;
    return `${protocol}//${hostname}:${port === "5000" ? "4005" : port}`;
}

export const handleErrors = async (response) => {
    if (!response.ok) {
        const message = await response.json().then(res => res.message);
        throw Error(message);
    }
    return response;
}

/* Handle File name */

export const getFileNameFromHeaders = (headers) => {
    const xFileName = headers.get("X-file-name");
    if (xFileName) return xFileName;
    let contentDisposition = headers.get("Content-Disposition");
    if (contentDisposition) {
        contentDisposition = contentDisposition.split('filename=');
        if (contentDisposition.length <= 1) return '';
        return JSON.parse(contentDisposition[1]);
    }
    return '';
};

export const getFileName = response => {
    let output = 'new file.mp3'
    if (response && response.headers) { 
        const fileNameFromHeaders = getFileNameFromHeaders(response.headers);
        output = fileNameFromHeaders ? fileNameFromHeaders : output;
    };
    return output
};