<template>
	<div class="col-span-1 border transition delay-75 ease-in hover:border-tgo-teal-500 bg-white shadow-sm rounded-md space-y-3">
		<div class="flex items-center justify-between bg-gray-50 rounded-t-md py-3">
			<div class="text-xs px-2 py-1 font-semibold">{{ data.desAccountNumber }}</div>
			<div class="px-2 text-xs flex items-center gap-1 text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				{{ dateLocale(data.createdAt) }}
			</div>
		</div>

		<div class="px-2">
			<textarea :disabled="!edit" v-model="data.accountName" class="px-2 py-1 border w-full text-center" :class="{ 'cursor-not-allowed': !edit, 'cursor-text': edit }" />
			<button v-if="!edit" class="text-xs underline text-blue-500 hover:text-yellow-500" @click="edit = true">{{ $t("button.edit") }}</button>

			<div v-if="edit" class="flex items-center gap-2">
				<button class="text-xs underline text-gray-500 hover:text-gray-600" @click="edit = false">
					{{ $t("button.cancel") }}
				</button>
				<button class="text-xs underline text-blue-500 hover:text-green-500" @click="editName(data._id, data.accountName, index)">
					{{ $t("button.ok") }}
				</button>
			</div>
		</div>
		<div class="px-2 text-sm">
			<p>
				{{ $t("account.table.header.number_of_projects") }}: <span class="text-gray-500 font-semibold">{{ groupedProject(data.accountVintages) }}</span>
			</p>
			<p>
				{{ $t("account.table.header.credit") }}: <span class="text-gray-500 font-semibold">{{ data.totalCredits.toLocaleString() }}</span>
			</p>
		</div>

		<div class="flex items-center text-xs border-t divide-x rounded-b-md">
			<div class="w-1/2 p-3 hover:bg-gray-200 rounded-bl-md flex items-center justify-center cursor-pointer">
				<nuxt-link class="flex items-center justify-center gap-1" :to="localePath({ name: 'accounts-id', params: { id: data._id } })">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-blue-500">
						<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
						<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
					{{ $t("button.see") }}
				</nuxt-link>
			</div>
			<div class="w-1/2 p-3 hover:bg-gray-200 rounded-br-md flex items-center justify-center cursor-pointer">
				<button class="flex items-center justify-center gap-1" @click="deleteUser(data._id)">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash text-red-500" viewBox="0 0 16 16">
						<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
						<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
					</svg>
					{{ $t("account.button.remove") }}
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["data", "index"],
	data() {
		return {
			edit: false,
		};
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
		for (let i = 0; i < this.data.length; i++) {
			this.edit.push(false);
		}
	},
	methods: {
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		async editName(id, name) {
			const app = this;
			const form = {
				accountName: name,
			};
			app.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("editing"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			app.$swal.showLoading();
			await this.$axios
				.$put(`/api/v1/account/${id}`, form)
				.then((resp) => {
					// console.log(resp);
					app.$swal.close();
					app.edit = false

					this.$emit("reload");
					// app.dropdowns.account_types = resp;
				})
				.catch((err) => {
					console.log(err);
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
							.$delete(`/api/v1/account/${id}`)
							.then((resp) => {
								// console.log(resp);
								app.$swal.close();

								// app.form = resp;
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: this.$t("alert.title.success.delete"),
										confirmButtonColor: "#059669",
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
		groupedProject(data) {
			let grouped = this._.groupBy(data, "projectId");
			let credit = [];
			for (const [key, value] of Object.entries(grouped)) {
				credit.push(value);
			}
			return credit.length;
		},
	},
};
</script>

<style></style>
