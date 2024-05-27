<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr class="divide-x bg-tgo-teal-500 rounded">
					<template v-for="(item, idx) in table.head">
						<ApiHeadSlotDark :text="item.name" :align="item.align" :key="idx" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in form">
					<tr class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border divide-x" :key="index">
						<AccountDataSlot :text="datetime(data.createdAt)" align="center"></AccountDataSlot>

						<AccountDataSlot :text="data.fromAccountName" align="center"></AccountDataSlot>
						<AccountDataSlot :text="data.toAccountName" align="center"></AccountDataSlot>
						<AccountDataSlot :text="data.amount.toLocaleString()" align="center"></AccountDataSlot>
						<AccountDataSlot :text="data.remark" align="center"></AccountDataSlot>
						<AccountStatusSlot :status="data.status" align="center"></AccountStatusSlot>
					</tr>

					<!-- <tr tabindex="0" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300" :key="index + 'sum'">
						
					</tr> -->
				</template>
			</tbody>
		</table>
		<div class="bg-white w-full flex justify-center items-center py-5 rounded-b" v-if="form.length === 0">
			<span class="text-sm">{{ $t("no_data") }}</span>
		</div>
	</div>
</template>

<script>
	export default {
		name:'Transaction-Table',
		props: ["form"],
		data() {
			return {
				showModal: true,
				dataModal: {},
				number: 0,
				table: {
					head: [
						{
							name: this.$t("account.view.date_and_time"),
							align: "center",
							filterable: false,
						},

						{
							name: this.$t("account.view.transferor"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("account.view.transferee"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("account.view.credit"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("account.view.detailed"),
							align: "center",
							filterable: false,
						},
						{
							name: this.$t("account.view.status"),
							align: "center",
							filterable: false,
						},
					],
				},
			};
		},
		computed: {
			// fullName() {
			// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
			// },
		},
		mounted() {
			// console.log(this.loggedInUser, this.isAuthenticated)
			// console.log(this.form);
		},
		methods: {
			seePdf(value) {
				// console.log(value);
				this.dataModal = value;
				this.showModal = true;
			},
			dateToString(date) {
				const result = new Date(date).toLocaleDateString("th-TH", {
					year: "numeric",
					month: "long",
					day: "numeric",
				});
				return result;
			},
			dateLocale(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			},
			datetime(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			},
			sumCarbon() {
				let sum = 0;
				// console.log(this.form);
				this.form.carbon_credit_cert.forEach((element) => {
					sum += element.amount;
				});
				return sum.toLocaleString();
			},
		},
	};
</script>
