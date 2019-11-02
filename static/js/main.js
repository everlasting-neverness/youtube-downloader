window.onload = function() {
    const downloadForm = document.querySelector('.form');
    const urlInput = this.document.getElementById('url_to_download');
    downloadForm.addEventListener('submit', e => {
        e.preventDefault();
        const urlToDownload = urlInput.value;
        if (!urlToDownload) {
            return false;
        }
        fetch(`/download?url_to_download=${urlToDownload}`)
            .then(res => {
                console.log(res);
            })
            .catch(err => {
                console.log(err);
            });
    });
};
