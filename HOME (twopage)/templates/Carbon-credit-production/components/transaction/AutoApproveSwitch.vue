<template>
	<div class="w-14 h-7 rounded-full relative cursor-pointer bg-gray-300" :class="{ 'bg-green-500': autoValue == 1, 'cursor-not-allowed': !this.$auth.user.scope.includes('settingManagement') }" @click="swicthLang">
		<div class="bg-white w-8 h-6 shadow-sm rounded-full absolute z-20 top-0.5 left-0.5 transform flex items-center justify-center duration-100 delay-75" :class="{ 'translate-x-0': autoValue == 0, 'translate-x-5': autoValue == 1 }"></div>
	</div>
</template>

<script>
	export default {
		name: "auto-approve-widget",
		data() {
			return {
				autoValue: 0,
			};
		},
		mounted() {
			this.getAutoApproveValue();
		},
		methods: {
			swicthLang() {
				if (!this.$auth.user.scope.includes("settingManagement")) {
					return;
				} else if (this.autoValue === 0) {
					this.autoValue = 1;
				} else {
					this.autoValue = 0;
				}
				this.setAutoApproveValue();
			},
			async getAutoApproveValue() {
				this.autoValue = await this.$axios
					.$get(`/api/v1/setting/auto-approve-setting`)
					.then((resp) => resp.autoApproveTransaction)
					.catch((err) => {
						console.log(err);
					});
			},
			confirmText() {
				if (this.$i18n.locale === "th") {
					if (this.autoValue === 1) return this.$t("sweetalert.transaction.setting.confirm.sub_title", { action: "เปิด" });
					else return this.$t("sweetalert.transaction.setting.confirm.sub_title", { action: "ปิด" });
				} else {
					if (this.autoValue === 1) return this.$t("sweetalert.transaction.setting.confirm.sub_title", { action: "enable" });
					else return this.$t("sweetalert.transaction.setting.confirm.sub_title", { action: "disable" });
				}
			},
			successTitle() {
				if (this.autoValue === 1) return this.$t("sweetalert.transaction.setting.success.enabled.title");
				else return this.$t("sweetalert.transaction.setting.success.disabled.title");
			},
			successText() {
				if (this.autoValue === 1) return this.$t("sweetalert.transaction.setting.success.enabled.sub_title");
				else return this.$t("sweetalert.transaction.setting.success.disabled.sub_title");
			},
			setAutoApproveValue() {
				const app = this;
				this.$swal
					.fire({
						icon: "info",
						iconColor: "#10b981",
						iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
`,
						title: this.$t("sweetalert.transaction.setting.confirm.title"),
						text: this.confirmText(),
						showCancelButton: true,

						confirmButtonColor: "#10b981",
						confirmButtonText: this.$t("button.confirm"),
						cancelButtonText: this.$t("button.cancel"),
						reverseButtons: true,
					})
					.then((result) => {
						if (result.isConfirmed) {
							app.$swal.fire({
								title: this.$t("sweetalert.waiting"),
								text: this.$t("saving"),
								allowOutsideClick: false,
								showCloseButton: false,
							});
							app.$swal.showLoading();
							app.$axios
								.$put(`/api/v1/setting/auto-approve-setting`, {
									name: "autoApproveTransaction",
									value: app.autoValue,
								})
								.then((resp) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "success",
										iconColor:'#059669',
										confirmButtonColor: "#059669",
										title: this.successTitle(),
										text: this.successText(),
										
									});
								})
								.catch((err) => {
									app.$swal.close();
									app.$swal.fire({
										icon: "error",
										title: app.$t("sweetalert.transaction.setting.error.title"),
										text: app.$t("sweetalert.transaction.setting.error.sub_title"),
										timer: 2000,
										timerProgressBar: true,
									});
									if (app.autoValue === 0) {
										app.autoValue = 1;
									} else {
										app.autoValue = 0;
									}
									console.log(err);
								});
						} else {
							if (this.autoValue === 0) {
								this.autoValue = 1;
							} else {
								this.autoValue = 0;
							}
						}
					});
			},
		},
	};
</script>

<style></style>
