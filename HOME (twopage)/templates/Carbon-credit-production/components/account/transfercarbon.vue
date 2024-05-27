<template>
	<div>
		<div class="grid grid-cols-3 gap-4 p-4 bg-gray-50 mt-2">
			<div class="col-span-1">
				<span class="font-semibold">{{ $t("account.view.transferee") }}</span>
			</div>
			<div class="col-span-2">
				<v-select :options="dropdowns.account" :reduce="(text) => text.value" label="text_show" v-model="transfer.toAccountNumber" />
			</div>
			<div class="col-span-1">
				<span class="font-semibold">{{ $t("account.view.credit") }}</span>
			</div>
			<div class="col-span-2">
				<input type="number" v-model.number="transfer.amount" class="w-full border bg-gray-50 px-3 py-1" />
			</div>
			<div class="col-span-1">
				<span class="font-semibold">{{ $t("account.transfer.remark") }}</span>
			</div>
			<div class="col-span-2">
				<input type="text" v-model="transfer.remark" class="w-full border bg-gray-50 px-3 py-1" />
			</div>
			<div class="col-span-2"></div>
			<div class="col-span-1 flex justify-end">
				<button @click="Transfer_credits()" class="px-2 py-1.5 bg-tgo-teal-500 w-1/2 hover:bg-tgo-teal-600 shadow-sm rounded justify-center text-white flex items-center">{{ $t("account.transfer.transfer") }}</button>
			</div>
		</div>
	</div>
</template>
<script>
	export default {
		props: ["form"],
		data() {
			return {
				dropdowns: {
					email: [],
					account: [],
					userScopes: [],
				},
				transfer: {
					toAccountNumber: null,
					amount: 0,
					year: null,
					remark: "",
					fromAccountNumber: this.id,
				},
				credit: [],
			};
		},
		watch: {
			"projectSelect.toggle": function (val) {
				this.transfer.amount = 0;
			},
			"transfer.amount": function (val) {
				if (val > this.credit[this.projectSelect.arr[0]][this.projectSelect.arr[1]].amount) {
					this.transfer.amount = this.credit[this.projectSelect.arr[0]][this.projectSelect.arr[1]].amount;
				}
				if (val < 0) {
					this.transfer.amount = 0;
				}
			},
		},
		mounted() {
			let grouped = this._.groupBy(this.form, "projectId");
			for (const [key, value] of Object.entries(grouped)) {
				// console.log(`${key}: ${value}`);
				this.credit.push(value);
			}
			console.log(this.credit);
			this.getaccount();
		},
		methods: {
			async getaccount() {
				const app = this;

				await this.$axios
					.$get(`/api/v1/dropdown/account-numbers`)
					.then((resp) => {
						// console.log(resp);
						app.dropdowns.account = resp;
						this._.remove(app.dropdowns.account, {
							value: this.id,
						});
						app.dropdowns.account.map(function (x) {
							return (x.text_show = x.value + " " + x.accountName);
						});
					})
					.catch((err) => {
						console.log(err);
					});
			},
			Transfer_credits() {
				const app = this;
				if (this.transfer.toAccountNumber === null) {
					this.$toast.error(app.$t("account.transfer.Please_select_a_transferee"));
					setTimeout(this.$toast.clear, 3000);
					return;
				}
				if (this.profile) {
					app.$swal
						.fire({
							title: this.$t("alert.title.warning"),
							text: app.$t("account.transfer.Do_you_want_to_transfer_credit"),
							showCancelButton: true,

							confirmButtonColor: "#4CA365",
							confirmButtonText: `${app.$t("button.confirm")}`,
							cancelButtonText: `${app.$t("button.cancel")}`,
						})
						.then((result) => {
							if (result.isConfirmed) {
								app.transfer.projectId = app.credit[app.projectSelect.arr[0]][app.projectSelect.arr[1]].projectId;
								app.transfer.year = app.credit[app.projectSelect.arr[0]][app.projectSelect.arr[1]].year;
								this.$axios
									.$post(`/api/v1/auth/account/transfer`, app.transfer)
									.then((resp) => {
										console.log(resp);
										app.$toast.success(app.$t("account.transfer.successful_transfer"));
										setTimeout(app.$toast.clear, 3000);
										// this.$emit("getAccount");
										location.reload();
										// app.dropdowns.account = resp;
									})
									.catch((err) => {
										console.log(err);
									});
							}
						});
				} else {
					app.$swal
						.fire({
							title: this.$t("alert.title.warning"),
							text: app.$t("account.transfer.Do_you_want_to_transfer_credit"),
							showCancelButton: true,

							confirmButtonColor: "#4CA365",
							confirmButtonText: `${app.$t("button.confirm")}`,
							cancelButtonText: `${app.$t("button.cancel")}`,
						})
						.then((result) => {
							if (result.isConfirmed) {
								app.transfer.projectId = app.credit[app.projectSelect.arr[0]][app.projectSelect.arr[1]].projectId;
								app.transfer.year = app.credit[app.projectSelect.arr[0]][app.projectSelect.arr[1]].year;
								this.$axios
									.$post(`/api/v1/account/transfer`, app.transfer)
									.then((resp) => {
										console.log(resp);
										app.$toast.success(app.$t("account.transfer.successful_transfer"));
										setTimeout(app.$toast.clear, 3000);
										// this.$emit("getAccount");
										location.reload();
										// app.dropdowns.account = resp;
									})
									.catch((err) => {
										console.log(err);
									});
							}
						});
				}
			},
		},
	};
</script>
