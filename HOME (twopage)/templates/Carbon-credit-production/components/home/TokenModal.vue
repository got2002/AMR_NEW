<template>
	<div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-60 flex items-center justify-center">
		<div class="mx-auto container bg-white rounded shadow-sm p-4 w-4/12 space-y-4">
			<div class="flex justify-between items-center">
				<p class="text-xl font-bold">{{ $t("home.modal.title") }}</p>
				<button @click="$emit('close')" class="bg-white px-3 py-1 border border-gray-300 hover:bg-gray-50 rounded">{{ $t("button.close") }}</button>
			</div>
			<div>
				<p class="text-sm font-thin">{{ $t("home.modal.subtitle") }}</p>
			</div>
			<div>
				<label>{{ $t("home.modal.label.token") }}</label>
				<div class="p-4 bg-gray-50 border border-gray-200 flex items-center justify-between relative">
					<div v-show="loading" class="absolute z-10 bg-black bg-opacity-60 flex items-center justify-center h-full w-full top-0 left-0">
						<p class="text-white">{{ $t("loading") }}</p>
					</div>

					<input readonly @focus="$event.target.select()" ref="clone" :title="$t('click_copy')" @click="copyToClipboard" class="text-sm w-full break-words cursor-pointer" id="myToken" v-model="token" />
				</div>
			</div>
			<div class="flex justify-end">
				<button @click="getToken()" class="px-4 py-2 rounded shadow-sm text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-400">{{ $t("button.create_token") }}</button>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["open"],
		data() {
			return {
				token: "",
				loading: false,
			};
		},
		watch: {
			open() {
				this.checkExpireToken();
			},
		},
		mounted() {
			this.checkExpireToken();
		},
		methods: {
			checkExpireToken() {
				const tokenTimestamp = this.$auth.$storage.getLocalStorage("timestamp");

				const diffDay = this.$dayjs(new Date()).diff(tokenTimestamp, "minute");
				if (diffDay >= 15) {
					this.getToken();
				} else {
					this.token = this.$auth.$storage.getLocalStorage("request_sync_token");
				}
			},
			copyToClipboard() {
				const copyText = document.getElementById("myToken");
				this.$refs.clone.focus();
				try {
					document.execCommand("copy");
					this.$toast.success(this.$t("toast.copy.success"));
				} catch (error) {
					this.$toast.error(this.$t("toast.copy.fail"));
				}

				setTimeout(this.$toast.clear, 3000);
			},
			getToken() {
				const app = this;
				this.loading = true;
				this.$axios
					.$get(`/api/v1/auth/request-sync-token`)
					.then((resp) => {
						app.loading = false;
						app.token = resp.token;
						app.$auth.$storage.setLocalStorage("request_sync_token", resp.token);
						app.$auth.$storage.setLocalStorage("timestamp", new Date());
					})
					.catch((err) => {
						app.loading = false;
						console.log(err);
					});
			},
		},
	};
</script>

<style></style>
