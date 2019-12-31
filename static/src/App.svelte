<script>
    export let initialUrl;
    import { handleErrors, getFileName, getFileNameFromHeaders } from './utils/siteUtils.js';

    let urlToDownload = '',
        errorMessage = '';

	const downloadFile = (name, contents) => {
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
    };

	const submitHandler = e => {
		e.preventDefault();

        errorMessage = '';

        if (!urlToDownload) {
            return false;
        }
        let filename = '';
        fetch(`${initialUrl}/download?url_to_download=${urlToDownload}`)
            .then(handleErrors)
            .then(res => {
                filename = getFileName(res);
                return res.blob()
            })
            .then(data => {
                downloadFile(filename, data);
            })
            .catch(err => {
                console.log(err);
                errorMessage = err.message || 'There was an error in the app. Please try again later.';
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
    {#if errorMessage}
        <p>{errorMessage}</p>
    {/if}
</main>


<style>
	
</style>