<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-col items-start gap-4">
			<h2 class="mb-1 text-3xl font-bold">{{ $t("project.page_title") }}</h2>
			<div class="w-full grid lg:grid-cols-4 grid-cols-2 gap-4">
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.allProject')" :value="stat.total" :icon="1"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.verify')" :value="stat.verified" :icon="2"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.pending')" :value="stat.pending" :icon="3"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.concluded')" :value="stat.finish" :icon="4"></ProjectCarbonCreditAmount>
				</div>
			</div>

			<div class="w-full mt-4">
				<section class="flex items-center justify-between mb-2">
					<div class="flex items-end gap-2">
						<div class="">
							<select
								v-model="limit"
								@change="
									current_page = 1;
									getProject();
								"
								class="text-sm text-center py-1 border-b-2 bg-theme-black-50 hover:bg-white cursor-pointer rounded border-tgo-teal-500 bg-transparent outline-none focus:border-tgo-yellow-500 focus:bg-theme-white focus:shadow-sm focus:outline-none"
							>
								<option :value="10">10</option>
								<option :value="50">50</option>
								<option :value="100">100</option>
								<option :value="200">200</option>
							</select>
						</div>

						<div>
							<button @click="openFilter = !openFilter" class="bg-white flex items-center justify-center p-1 shadow-sm rounded" :class="{ 'bg-tgo-teal-500 text-white': openFilter }">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
								</svg>
							</button>
						</div>
						<div>
							<nuxt-link :to="localePath({ name: 'project-create' })" class="px-2 py-1 bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-sm rounded text-white flex items-center gap-1">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
								</svg>

								{{ $t("button.create_project") }}</nuxt-link
							>
						</div>
					</div>
				</section>
				<div v-if="openFilter" class="mb-2 w-full bg-white shadow-sm rounded">
					<ProjectFilter :filter="filter" :limit="meta.limit" @resetFilter="resetFilter()" @getProject="getProject()" />
				</div>
				<ProjectTable :project="project" @sort="getProject($event, 1)" />
			</div>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="isLoading"></loadingCarbon>
	</section>
</template>

<script>
export default {
	name: "ProjectIndex",
	layout: "DashboardLayout",
	middleware: ["auth"],

	data() {
		return {
			filter: {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: 0,
				max: null,
				vintage: [null, null],
				authUse: "",
			},

			current_page: 1,

			standard: "",
			province: "",

			isLoading: true,

			limit: 10,

			openFilter: false,
			provinces: [],
			project_types: [],
			autherizeduses: [],
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
			sort: { value: -1, key: "registration_date" },

			project: [],
		};
	},
	watch: {
		status() {
			this.sub_status = "";
		},
		"filter.min"(val) {
			if (val > this.filter.max) {
				this.filter.min = 0;
			}
		},
		"filter.max"(val) {
			if (val < this.filter.min && val >= this.meta.limit.maxTonnes) {
				this.filter.max = 1000000;
			}
		},
	},

	async mounted() {
		await this.getProvinces();

		await this.getStatPoject();
		await this.getProject({ key: "registration_date,project_id", value: "-1,-1" });
		this.isLoading = false;
	},
	methods: {
		resetFilter() {
			this.filter = {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: 0,
				max: 10000,
				vintage: [null, null],
				authUse: "",
			};
			this.openFilter = false;
			this.getProject({ key: "registration_date,project_id", value: "-1,-1" });
		},

		async getProvinces() {
			let app = this;
			app.isLoading = true;
			await this.$axios
				.$get(`/api/v1/dropdown/provinces`)
				.then((resp) => {
					// console.log(resp);
					app.provinces = resp;
				})
				.catch((errors) => {
					console.log(errors);
				});
		},

		getStatPoject() {
			const app = this;
			this.$axios.$get(`/api/v1/stats/projects`).then((resp) => {
				// console.log(resp)
				app.stat = resp;
			});
		},
		async getProject(sort = { key: "registration_date,project_id", value: "-1,-1" }, page = 1) {
			const app = this;
			// console.log(this.filter.searchText);
			this.sort = sort
			this.isLoading = true;
			this.current_page = page;

			let filter = `&sort=${sort.value}&sort_by=${sort.key}`;
			if (this.filter.searchText !== null && this.filter.searchText !== "") filter += `&search=${this.filter.searchText}`;
			if (this.filter.type !== null && this.filter.type !== "") filter += `&type=${this.filter.type}`;
			if (this.filter.status !== null && this.filter.status !== "") filter += `&status=${this.filter.status}`;
			if (this.filter.standard !== null && this.filter.standard !== "") filter += `&standard=${this.filter.standard}`;
			if (this.filter.sub_status !== null && this.filter.sub_status !== "") filter += `&sub_status=${this.filter.sub_status}`;
			if (this.province !== null && this.province !== "") filter += `&province=${this.province}`;
			if (this.filter.min !== null && this.filter.min !== "") filter += `&min=${this.filter.min}`;
			if (this.filter.max !== null && this.filter.max !== "") filter += `&max=${this.filter.max}`;
			if (this.filter.authUse !== null && this.filter.authUse !== "") filter += `&authorize_use=${this.filter.authUse}`;
			if (this.limit !== null && this.limit !== "") filter += `&limit=${this.limit}`;
			if (this.filter.vintage.length > 1 && !this.filter.vintage.includes(null)) filter += `&vintage_start=${this.$dayjs(this.filter.vintage[0]).format("YYYY-MM-DD")}&vintage_end=${this.$dayjs(this.filter.vintage[1]).format("YYYY-MM-DD")}`;
			await this.$axios
				.$get(`/api/v1/project?page=${this.current_page}` + filter)
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

		loadRequestByPage(pageNumber) {
			this.getProject(this.sort, pageNumber);
		},
	},
};
</script>

<style>
.mx-datepicker.mx-datepicker-range {
	width: 100% !important;
}
</style>
