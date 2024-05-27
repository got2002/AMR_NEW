<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1">
		

		
		<template v-for="(data, index) in form.reduction_methods">
			<div :key="index+'1'" class="col-span-1 bg-theme-black-50 bg-opacity-50 pt-4 px-4 gap-3 mt-5">
				<div class="flex">
					<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.name") }}:</div>
					<div class="px-2 text-sm break-words">
						{{ data.name }}
					</div>
				</div>
				<div class="flex">
					<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.document_version") }}:</div>
					<div class="px-2 text-sm break-words">
						{{ data.document_version }}
					</div>
				</div>
				<!-- <div class="flex">
					<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.description") }}:</div>
					<div class="px-2 text-sm">
						{{ data.description }}
					</div>
				</div> -->
			</div>
			<div :key="index+'2'" class="bg-theme-black-50 bg-opacity-50 pb-4 px-4 gap-3">
				<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.description") }}</div>
				<div class="text-sm break-words">{{ data.description }}</div>
			</div>
		</template>
		<div v-if="form.reduction_methods.length == 0" class="outline-none text-xs h-16 bg-gray-100 hover:bg-theme-green-100 align-middle cursor-pointer border border-theme-black-300">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form"],
	data() {
		return {
			table: {
				head: [
					{
						name: this.$t("project.create_page.reduction_methods.name"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.create_page.reduction_methods.document_version"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.create_page.reduction_methods.description"),
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
	},
	methods: {
		checkfile(filename) {
			let parts = filename.split(".");
			parts = parts[parts.length - 1];
			return parts.toLowerCase();
		},
		BaseUrl(url) {
			return process.env.baseUrl + url;
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
		},
		sumCarbon() {
			let sum = 0;
			// console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum;
		},
	},
};
</script>