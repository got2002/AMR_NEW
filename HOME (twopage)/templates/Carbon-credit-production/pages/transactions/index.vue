<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-col items-start gap-4">
			<div class="flex items-center justify-between mb-1 w-full">
				<div>
					<h2 class="text-3xl font-bold">{{ $t("transaction.page_title") }}</h2>
					<div class="mb-1 text-sm font-normal opacity-50">{{ $t("show_data", { from: meta.current_page * 10 - 9, to: meta.current_page * 10 - (10-project.length), all: meta.total }) }}</div>
				</div>

				<div class="flex items-center gap-2">
					<span>{{ $t("transaction.setting.auto_approve") }}</span>
					<TransactionAutoApproveSwitch></TransactionAutoApproveSwitch>
				</div>
			</div>

			<div class="w-full mt-4">
				<section class="flex items-center justify-between mb-2">
					<div class="flex items-center gap-2">
						<select v-model="limit" @change="getTransaction(1)" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
						<select v-model="status" @change="getTransaction(1)" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="-1">{{ statusText(-1) }}</option>
							<option :value="0">{{ statusText(0) }}</option>
							<option :value="1">{{ statusText(1) }}</option>
							<option :value="2">{{ statusText(2) }}</option>
							<option :value="3">{{ statusText(3) }}</option>
							<option :value="4">{{ statusText(4) }}</option>
							<option :value="5">{{ statusText(5) }}</option>
						</select>
						<div class="w-60 border border-gray-200 rounded">
							<DatePicker @change="getTransaction()" v-model="transferDate" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" :lang="$i18n.locale" range format="DD MMM YYYY" :formatter="thaiformatter" value-type="date" input-class="text-center text-sm px-2 py-1.5 w-full outline-none rounded" />
						</div>
					</div>

					<div>
						<div class="flex items-center relative">
							<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
								</svg>
							</span>
							<input type="text" v-model="search" @change="getTransaction()" :placeholder="$t('transaction.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
						</div>
					</div>
				</section>

				<TransactionTable :project="project" @reload="getTransaction()" :loading="isLoading"/>
			</div>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="isLoading"></loadingCarbon>
	</section>
</template>

<script>
	import thaiformatter from "../../mixins/thaiformatter";
	export default {
		name: "CreditManagement",
		layout: "DashboardLayout",
		middleware: ["auth"],
		mixins: [thaiformatter],

		data() {
			return {
				isLoading: true,

				limit: 10,
				status: 0,
				search: "",
				transferDate: [],

				meta: {
					pages: 1,
					current_page: 1,
					total: 1,
				},
				stat: {
					total: 0,
					verified: 0,
					pending: 0,
					finish: 0,
				},
				sort: -1,
				sort_by: "registration_date",
				
				project: [],
			};
		},
		watch: {
			status() {
				this.sub_status = "";
			},
		},
		async mounted() {
			await this.getTransaction();
			this.isLoading = false;
		},
		methods: {
			resetFilter() {},
			statusText(status) {
				switch (status) {
					case -1:
						if (this.$i18n.locale === "th") return "สถานะทั้งหมด";
						else return "all status";
					case 0:
						if (this.$i18n.locale === "th") return "รอดำเนินการ";
						else return "pending";
					case 1:
						if (this.$i18n.locale === "th") return "กำลังดำเนินการโอน";
						else return "in-progress";
					case 2:
						if (this.$i18n.locale === "th") return "โอนสำเร็จ";
						else return "completed";
					case 3:
						if (this.$i18n.locale === "th") return "โอนไม่สำเร็จ";
						else return "failed";
					case 4:
						if (this.$i18n.locale === "th") return "ยกเลิกการโอน";
						else return "cancelled";
					case 5:
						if (this.$i18n.locale === "th") return "ปฏิเสธการโอน";
						else return "rejected";

					default:
						break;
				}
			},

			async getTransaction(page = 1) {
				const app = this;
				app.isLoading = true;
				this.current_page = page;
				let dateFilter = ``;
				if (this.transferDate.length === 2 && !this.transferDate.includes(null)) {
					dateFilter = `date_start=${this.$dayjs(this.transferDate[0]).format("YYYY-MM-DD")}&date_end=${this.$dayjs(this.transferDate[1]).format("YYYY-MM-DD")}`;
				}
				await this.$axios
					.$get(`/api/v1/transaction?limit=${this.limit}&page=${this.current_page}&search=${this.search}&status=${this.status}&${dateFilter}`)
					.then((resp) => {
						// console.log(resp);
						app.project = resp.data;
						app.meta = resp.meta;
						// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
						// this.$router.push("/users/userManagement");
						// setTimeout(this.$toast.clear, 3000);
						app.isLoading = false;
					})
					.catch((errors) => {
						console.log(errors);
						// this.$toast.error(errors.response.data.errors);
						// setTimeout(this.$toast.clear, 3000);
						app.isLoading = false;
					});
			},

			async loadRequestByPage(pageNumber) {
				await this.getTransaction(pageNumber);
			},
		},
	};
</script>

<style>
	.mx-datepicker.mx-datepicker-range {
		width: 100% !important;
	}
</style>
