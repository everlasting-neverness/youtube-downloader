import { getInitialUrlForRequests } from './utils/siteUtils.js';
import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		initialUrl: getInitialUrlForRequests()
	}
});

export default app;