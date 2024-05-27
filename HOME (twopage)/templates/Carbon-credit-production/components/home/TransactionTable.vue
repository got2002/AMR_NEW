<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 2xl:overflow-hidden overflow-x-scroll">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr>
					<template v-for="(header, idx) in table.head">
						<HomeHeaderSlot :key="idx" :header="header"></HomeHeaderSlot>
					</template>
				</tr>
			</thead>
			<tbody>
				<template v-for="(data, index) in transaction">
					<tr :key="index" class="outline-none text-xs hover:bg-gray-50 rounded-md align-middle bg-white h-12">
						<HomeCreditRowData class="rounded-l-md" :text="datetime(data.createdAt)" align="center"></HomeCreditRowData>
						
					
						<HomeCreditRowDataName :text="data.fromAccountName" :sub_text="data.fromAccountNumber" align="center"></HomeCreditRowDataName>
						<HomeCreditRowDataName :text="data.toAccountName" :sub_text="data.toAccountNumber" align="center"></HomeCreditRowDataName>
						<HomeCreditRowData :text="data.amount.toLocaleString()" align="center"></HomeCreditRowData>
						<HomeCreditRowData :text="data.remark" align="center"></HomeCreditRowData>
						<TransactionStatusSlot class="rounded-r-md" :status="data.status" align="center"></TransactionStatusSlot>

					
					</tr>
					<tr :key="index + 'blank'">
						<td colspan="6" class="py-1"></td>
					</tr>
				</template>
			</tbody>
		</table>
	

		<div v-if="transaction.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded ">
			<div class="flex justify-center items-center">
				<span class="font-medium text-sm text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["transaction"],
		data() {
			return {
			
				modalOpen: false,
				table: {
					head: [
						{
							name: this.$t("account.view.date_and_time"),
							align: "center",
							sortable: false,
							colspan: 1,
							rowspan: 1,
						},
						{
							name: this.$t("account.view.transferor"),
							align: "center",
							sortable: false,
							colspan: 1,
							rowspan: 1,
						},

						{
							name: this.$t("account.view.transferee"),
							align: "center",
							sortable: false,
							colspan: 1,
							rowspan: 1,
						},

						{
							name: this.$t("account.view.credit"),
							align: "center",
							sortable: false,
							colspan: 2,
							rowspan: 2,
						},

						{
							name: this.$t("account.view.detailed"),
							align: "center",
							sortable: false,
							colspan: 1,
							rowspan: 1,
						},

						{
							name: this.$t("account.view.status"),
							align: "center",
							sortable: false,
							colspan: 1,
							rowspan: 1,
						},
					],
				},
				selectInfo: {},
				showCreditLabel: [],
			};
		},
		computed: {
			// fullName() {
			// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
			// },
		},
		mounted() {
			// console.log(this.loggedInUser, this.isAuthenticated)
			this.showCreditValue();
		},
		watch: {
			"project.length"(value) {
				this.showCreditValue();
			},
		},
		methods: {
			yearVintage(year) {
				if (this.$i18n.locale === "th") {
					return year + 543;
				}
				return year;
			},
			reloadData() {
				this.modalOpen = false;
				this.$emit("reload");
			},
			showCreditValue() {
				const app = this;
				app.showCreditLabel = this._.map(this.project, (item) => {
					return { show: false };
				});
			},
			openModalEvt(data) {
				this.selectInfo = data;
				this.modalOpen = true;
			},

			projectName(data) {
				if (this.$i18n.locale === "th") {
					return data.thai;
				} else {
					return data.english;
				}
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
		},
	};
</script>
<style>
	.table-mim-w {
		min-width: 100%;
	}
</style>
