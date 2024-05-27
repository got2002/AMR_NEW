<template>
	<section class="pt-2 pb-4">
		<div v-if="!isLoading" class="flex flex-col items-start gap-4">
			<div>
				<h2 class="mb-1 text-3xl font-bold">{{ $t("credit.page_title") }}</h2>
			</div>

			<div class="w-full mt-4">
				<section class="flex items-center justify-between mb-2">
					<div class="flex items-center gap-2">
						<select v-model="limit" @change="getProject()" class="text-sm text-center border-2 border-tgo-teal-400 px-2 py-0.5 bg-white">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
						<div class="w-40 border-2 border-tgo-teal-400">
							<DatePicker @change="getProject()" :placeholder="$t('credit.table.header.vintage_year')" type="year" v-model="vintage_year" format="DD MMM YYYY" :formatter="yearFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1 w-full outline-none"></DatePicker>
						</div>
						<div class="flex items-center w-52 text-sm">
							<input @change="getProject()" v-model="min" :placeholder="$t('credit.min')" class="px-2 py-1 border-2 border-r-0 border-tgo-teal-400 text-center outline-none w-24" />
							<div class="border-t-2 border-b-2 border-tgo-teal-400 bg-tgo-teal-400 py-1 text-center w-4">-</div>
							<input @change="getProject()" v-model="max" :placeholder="$t('credit.max')" class="px-2 py-1 border-2 border-l-0 border-tgo-teal-400 text-center outline-none w-24" />
						</div>
					</div>

					<div>
						<div class="flex items-center relative">
							<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
								</svg>
							</span>
							<input type="text" v-model="search" @change="getProject()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1 pl-10 pr-4 border-2 border-tgo-teal-400 outline-none" />
						</div>
					</div>
				</section>

				<CreditTable :project="project" :accountNumber="accountNumber" @reload="getProject(1)" @sort="getProject(1,$event)"/>
			</div>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />

		<div v-if="!isLoading" class="w-full mt-4">
			<div class="flex justify-between items-center mb-2">
				<p class="text-lg font-bold">{{ $t("account.view.transaction") }}</p>
				<div class="flex items-center gap-2">
					<div class="flex items-center relative">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1.5">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input type="text" v-model="transaction_filter.search" @change="getTransaction()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1 pl-10 pr-4 border-2 border-tgo-teal-400 outline-none" />
					</div>
					<select v-model="transaction_filter.limit" @change="getTransaction()" class="text-sm text-center border-2 border-tgo-teal-400 px-2 py-0.5 bg-white">
						<option :value="10">10</option>
						<option :value="50">50</option>
						<option :value="100">100</option>
						<option :value="200">200</option>
					</select>
				</div>
			</div>

			<AccountTableTransaction :form="transaction"></AccountTableTransaction>
			<PaginationBar :meta="transaction_meta" @loadRequestByPage="changeTransactionPage" />
		</div>
		<loadingCarbon v-if="isLoading"></loadingCarbon>
		<loadingCarbon v-if="refreshData"></loadingCarbon>
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
				refreshData: false,

				min: null,
				max: null,
				limit: 10,
				vintage_year: null,
				search: "",

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
				project_types_ccmgm: ["พลังงานหมุนเวียนหรือพลังงานที่ใช้ทดแทนเชื้อเพลิงฟอสซิล", "การเพิ่มประสิทธิภาพการผลิตไฟฟ้าและการผลิตความร้อน", "การใช้ระบบขนส่งสาธารณะ", "การใช้ยานพาหนะไฟฟ้า", "การเพิ่มประสิทธิภาพเครื่องยนต์", "การเพิ่มประสิทธิภาพการใช้พลังงานในอาคารและโรงงาน และในครัวเรือน", "การปรับเปลี่ยนสารทำความเย็นธรรมชาติ", "การใช้วัสดุทดแทนปูนเม็ด", "การจัดการขยะมูลฝอย", "การจัดการน้ำเสียชุมชน", "การนำก๊าซมีเทนกลับมาใช้ประโยชน์", "การจัดการน้ำเสียอุตสาหกรรม", "การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร", "การดักจับ กักเก็บ และ/หรือใช้ประโยชน์จากก๊าซเรือนกระจก", "ประเภทอื่นๆ"],
				project: [],
				accountNumber: "",
				transaction: [],
				transaction_meta: {
					pages: 1,
					current_page: 1,
					total: 1,
				},
				transaction_filter: {
					limit: 10,
					search: "",
				},
			};
		},
		watch: {
			status() {
				this.sub_status = "";
			},
		},
		async mounted() {
			await this.getProject(1);
			await this.getTransaction();
			this.isLoading = false;
		},
		methods: {
			changeTransactionPage(page) {
				this.getTransaction(page);
			},
			getTransaction(page = 1) {
				const app = this;
				app.refreshData = true;
				this.transaction_current_page = page;
				this.$axios
					.$get(`/api/v1/credit/transaction?limit=${this.transaction_filter.limit}&page=${this.transaction_current_page}&search=${this.transaction_filter.search}`)
					.then((resp) => {
						app.transaction = resp.data;
						app.transaction_meta = resp.meta;
						app.refreshData = false;
					})
					.catch(() => {
						app.$toast.error(app.$t("toast.loading.error"));
						setTimeout(app.$toast.clear, 3000);
						app.refreshData = false;
					});
			},

			async getProject(page = 1,sort={key:'vintage_year',value:0}) {
				const app = this;
				app.isLoading = true;
				this.current_page = page;
				let yearVintage = "";
				if (this.vintage_year !== null) {
					yearVintage = this.$dayjs(this.vintage_year).format("YYYY");
				}
				await this.$axios
					.$get(`/api/v1/credit/table?limit=${this.limit}&page=${this.current_page}&year=${yearVintage}&min=${this.min}&max=${this.max}&search=${this.search}&sortKey=${sort.key}&sortValue=${sort.value}`)
					.then((resp) => {
						// console.log(resp);
						app.project = resp.data;
						app.accountNumber = resp.desAccountNumber;
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
				await this.getProject(pageNumber);
			},
		},
	};
</script>

<style>
	.mx-datepicker.mx-datepicker-range {
		width: 100% !important;
	}
</style>
