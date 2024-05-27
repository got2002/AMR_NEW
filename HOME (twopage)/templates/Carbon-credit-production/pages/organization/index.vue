<template>
	<section class="pt-2 pb-4">
		<div class="flex flex-col items-start gap-4">
			<div>
				<h2 class="mb-1 text-3xl font-bold">{{ $t("organization.page_title") }}</h2>
				<div class="mb-1 text-sm font-normal opacity-50">{{ $t("show_data", { from: meta.current_page * 10 - 9, to: meta.current_page * 10 - (10 - table.data.length), all: meta.total }) }}</div>
			</div>
			<div class="flex items-center justify-between w-full">
				<div class="flex items-center gap-2">
					<select @change="getOrganization()" v-model="limit" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
						<option :value="10">10</option>
						<option :value="50">50</option>
						<option :value="100">100</option>
					</select>
					<div class="relative">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 absolute top-0 left-0 ml-2 mt-2 text-gray-400">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
						</svg>

						<input v-model="search" @change="getOrganization()" :placeholder="`${$t('organization.filter.search')}...`" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
					</div>
				</div>
				<nuxt-link class="px-3 p-1.5 bg-tgo-teal-500 text-white shadow-sm flex items-center gap-1 rounded" :to="localePath({ name: 'organization-create' })">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
					</svg>

					{{ $t("button.add") }}
				</nuxt-link>
			</div>
			<div class="w-full">
				<OrganizationTable :data="table" @reload="getOrganization()"></OrganizationTable>
			</div>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="loading"></loadingCarbon>
	</section>
</template>

<script>
export default {
	name: "OrganizationPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	data() {
		return {
			meta: {
				pages: 0,
				current_page: 1,
				total: 0,
			},

			logs: [],
			current_page: 1,
			limit: 10,
			period: [],
			search: "",
			loading: true,
			table: {
				headers: [
					{
						text: this.$t("organization.table.header.organization_number"),
						align: "center",
					},
					{
						text: this.$t("organization.table.header.organization_name"),
						align: "center",
					},
					{
						text: this.$t("organization.table.header.organization_type"),
						align: "center",
					},
					{
						text: this.$t("organization.table.header.member"),
						align: "center",
					},
					{
						text: this.$t("organization.table.header.tool"),
						align: "center",
					},
				],
				data: [],
			},
			// expandInfo:[],
		};
	},

	mounted() {
		this.getOrganization();
	},
	methods: {
		loadRequestByPage(page) {
			this.getOrganization(page);
		},
		dateTime(date) {
			return this.$moment(date).format("DD MMM YYYY (HH:mm:ss)");
		},
		getOrganization(page = 1) {
			const app = this;
			this.current_page = page;
			this.loading = true;

			this.$axios
				.$get(`/api/v1/organization?page=${this.current_page}&limit=${this.limit}&search=${this.search}`)
				.then((resp) => {
					app.table.data = resp.data;
					// app._.forEach(resp.data,item=>{
					// 	app.expandInfo.push(false)
					// })
					app.meta = resp.meta;
					app.loading = false;
				})
				.catch((err) => {
					console.log(err);
					app.loading = false;
				});
		},
	},
};
</script>

<style>
.border-gradient {
	border: 2px solid;
	border-image: linear-gradient(to right, #4da366, #1d73c9) 1;
}
</style>
