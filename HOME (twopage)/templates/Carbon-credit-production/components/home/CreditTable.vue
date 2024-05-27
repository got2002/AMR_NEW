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
				<template v-for="(data, index) in project">
					<tr :key="index" class="outline-none text-xs hover:bg-gray-50 rounded-md align-middle bg-white h-12 px-2">
						<HomeCreditRowData class="rounded-l-md" :text="'#' + data.project_id" align="center"></HomeCreditRowData>
						<HomeCreditRowData :text="projectName(data.project_name)" align="center">
							<template v-slot:data>
								<div class="w-full flex items-center justify-center">
									<div :title="projectName(data.project_name)" class="max-w-md truncate ">{{ projectName(data.project_name) }}</div>
								</div>
							</template>
						</HomeCreditRowData>
						<HomeCreditRowData :text="yearVintage(data.vintage_year)" align="center"></HomeCreditRowData>

						<CreditBlockMain :data="data"></CreditBlockMain>
						<HomeCreditRowData :text="data.total_blocks" align="center"></HomeCreditRowData>

						<HomeCreditActionSlot class="rounded-r-md" :data="data" @openModal="openModalEvt" @openCertificate="openCertificate"></HomeCreditActionSlot>
					</tr>
					<tr :key="index + 'blank'">
						<td colspan="6" class="py-1"></td>
					</tr>
				</template>
			</tbody>
		</table>
		<CreditTransferModal v-if="modalOpen" @close="modalOpen = false" @submit="reloadData" :accountNumber="accountNumber" :info="selectInfo"></CreditTransferModal>
		<CreditCertificateModal v-if="modalCertificateOpen" @close="modalCertificateOpen = false" :info="selectInfo2"></CreditCertificateModal>

		<div v-if="project.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded">
			<div class="flex justify-center items-center">
				<span class="font-medium text-sm text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["project", "accountNumber"],
		data() {
			return {
				sort: [0, 0, -1, 0],
				modalOpen: false,

				table: {
					head: [
						{
							name: this.$t("credit.table.header.project_id"),
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-20",
						},
						{
							name: this.$t("credit.table.header.project_title"),
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-80",
						},

						{
							name: this.$t("credit.table.header.vintage_year"),
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-20",
						},

						{
							name: this.$t("credit.table.header.block"),
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-80",
						},

						{
							name: this.$t("credit.table.header.credit_amount"),
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-20",
						},

						{
							name: "",
							align: "center",
							sortable: false,
							class: "bg-blue-500 w-40",
						},
					],
				},
				selectInfo: {},
				selectInfo2: {},
				showCreditLabel: [],
				modalCertificateOpen: false,
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
			openCertificate(data) {
				this.selectInfo2 = data;
				this.modalCertificateOpen = true;
			},
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
		},
	};
</script>
<style>
	.table-mim-w {
		min-width: 100%;
	}
</style>
