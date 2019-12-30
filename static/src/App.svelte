<script>
	let urlToDownload = '';

	const download_file = (name, contents) => {
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

	const getFileName = response => {
        let output = 'new file'
        if (response && response.headers) output = response.headers.get("X-file-name");
        return output
    };

	const submitHandler = e => {
		e.preventDefault();

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
	};
</script>

<main class="content">
	<h1>YouTube Downloader</h1>
	<p>You can put a youtube in the from bellow and download a file</p>
	<form class="form" action="/download" method="GET" on:submit={submitHandler}>
		<input type="text" name="url_to_download" id="url_to_download" bind:value={urlToDownload}>
		<button>Download</button>
	</form>
</main>


<style>
	
</style>