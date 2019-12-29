window.onload = function() {
    const downloadForm = document.querySelector('.form');
    const urlInput = document.getElementById('url_to_download');

    function download_file(name, contents) {
        const blob = new Blob([contents], {type: contents.mime_type});

        const dlink = document.createElement('a');
        dlink.download = name;
        dlink.href = window.URL.createObjectURL(blob);
        dlink.onclick = function(e) {
            // revokeObjectURL needs a delay to work properly
            var that = this;
            setTimeout(function() {
                window.URL.revokeObjectURL(that.href);
            }, 1500);
        };

        dlink.click();
        dlink.remove();
    }

    function getFileName(response) {
        let output = 'new file'
        if (response && response.headers) output = response.headers.get("X-file-name");
        return output
    };

    downloadForm.addEventListener('submit', e => {
        e.preventDefault();
        const urlToDownload = urlInput.value;
        if (!urlToDownload) {
            return false;
        }
        let filename = '';
        fetch(`/download?url_to_download=${urlToDownload}`)
            .then(res => {
                filename = getFileName(res);
                return res.blob()
            })
            .then(data => {
                download_file(filename, data);
            })
            .catch(err => {
                console.log(err);
            });
    });
};
