window.onload = function() {
    const downloadForm = document.querySelector('.form');
    const urlInput = document.getElementById('url_to_download');

    function download_file(name, contents) {
        var mime_type = "audio/mpeg";

        var blob = new Blob([contents], {type: mime_type});

        var dlink = document.createElement('a');
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
        fetch(`/download?url_to_download=${urlToDownload}`)
            .then(res => {
                download_file(getFileName(res), res);
            })
            .catch(err => {
                console.log(err);
            });
    });
};
