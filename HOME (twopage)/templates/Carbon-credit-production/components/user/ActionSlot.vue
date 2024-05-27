<template>
	<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
		<div v-if="status !== 0" class="w-full flex items-center justify-center gap-2">
			<nuxt-link :to="localePath({ name: 'users-id-info', params: { id: id } })">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-blue-500">
					<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
					<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
				</svg>
			</nuxt-link>
			<nuxt-link :to="localePath({ name: 'users-id-edit', params: { id: id } })">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square text-yellow-500" viewBox="0 0 16 16">
					<path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
					<path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
				</svg>
			</nuxt-link>

			<button @click="deleteUser(id)">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
					<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
					<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
				</svg>
			</button>
		</div>
		<div v-else class="w-full flex items-center justify-center">
			<nuxt-link class="flex items-center bg-tgo-teal-500 hover:bg-tgo-teal-600 px-2 py-1 rounded text-white" :to="localePath({ name: 'users-id', params: { id: id } })">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
				</svg>
				<span>{{ $t("button.see") }}</span>
			</nuxt-link>
		</div>
	</td>
</template>

<script>
export default {
	props: ["id", "status"],
	methods: {
		approve(approveValue) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: approveValue === 1 ? "#10b981" : "#ef4444",
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.default"),
					showCancelButton: true,

					confirmButtonColor: approveValue === 1 ? "#10b981" : "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),

					input: "email",

					inputPlaceholder: "typing here...",
					inputValidator: (value) => {
						if (!value && approveValue === 2) {
							return "You need to write something!";
						}
					},
				})
				.then((result) => {
					console.log(result);
					if (result.isConfirmed) {
						app.$axios
							.$post(`/api/v1/user/${this.id}/approval`, {
								status: approveValue,
								remark: result.value,
							})
							.then((resp) => {
								// console.log(resp);

								// app.form = resp;
								app.$swal.fire({
									icon: "success",
									iconColor: "#059669",
									confirmButtonColor: "#059669",
									title: this.$t("alert.title.success.default"),
									timer: 2000,
									timerProgressBar: true,
								});
								setTimeout(app.$emit("reload"), 3000);
							})
							.catch((err) => {
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.default"),
								});
								console.log(err);
							});
					}
				});
		},
		deleteUser(id) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#ef4444",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
								</svg>`,
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.delete"),
					showCancelButton: true,

					confirmButtonColor: "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("deleting"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$delete(`/api/v1/user/${id}`)
							.then((resp) => {
								// console.log(resp);

								// app.form = resp;
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: this.$t("alert.title.success.delete"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.$emit("reload");
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.delete"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>

<style></style>
