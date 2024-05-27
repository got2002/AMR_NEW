<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-2">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr class="divide-x divide-gray-400 border border-gray-400">
					<template v-for="(item, idx) in table.head">
						<ApiHeadSlotWhite :class="item.class" :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in form.additional_document">
					<tr :key="index" class="text-xs h-12 hover:bg-theme-green-100 align-middle divide-y divide-x divide-black">
						<td class="px-1 border-t border-black">
							<div class="w-full flex items-center">
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="bg-red-500" class="bi bi-file-earmark-pdf-fill" viewBox="0 0 16 16">
									<path d="M5.523 12.424c.14-.082.293-.162.459-.238a7.878 7.878 0 0 1-.45.606c-.28.337-.498.516-.635.572a.266.266 0 0 1-.035.012.282.282 0 0 1-.026-.044c-.056-.11-.054-.216.04-.36.106-.165.319-.354.647-.548zm2.455-1.647c-.119.025-.237.05-.356.078a21.148 21.148 0 0 0 .5-1.05 12.045 12.045 0 0 0 .51.858c-.217.032-.436.07-.654.114zm2.525.939a3.881 3.881 0 0 1-.435-.41c.228.005.434.022.612.054.317.057.466.147.518.209a.095.095 0 0 1 .026.064.436.436 0 0 1-.06.2.307.307 0 0 1-.094.124.107.107 0 0 1-.069.015c-.09-.003-.258-.066-.498-.256zM8.278 6.97c-.04.244-.108.524-.2.829a4.86 4.86 0 0 1-.089-.346c-.076-.353-.087-.63-.046-.822.038-.177.11-.248.196-.283a.517.517 0 0 1 .145-.04c.013.03.028.092.032.198.005.122-.007.277-.038.465z" />
									<path fill-rule="evenodd" d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2zm5.5 1.5v2a1 1 0 0 0 1 1h2l-3-3zM4.165 13.668c.09.18.23.343.438.419.207.075.412.04.58-.03.318-.13.635-.436.926-.786.333-.401.683-.927 1.021-1.51a11.651 11.651 0 0 1 1.997-.406c.3.383.61.713.91.95.28.22.603.403.934.417a.856.856 0 0 0 .51-.138c.155-.101.27-.247.354-.416.09-.181.145-.37.138-.563a.844.844 0 0 0-.2-.518c-.226-.27-.596-.4-.96-.465a5.76 5.76 0 0 0-1.335-.05 10.954 10.954 0 0 1-.98-1.686c.25-.66.437-1.284.52-1.794.036-.218.055-.426.048-.614a1.238 1.238 0 0 0-.127-.538.7.7 0 0 0-.477-.365c-.202-.043-.41 0-.601.077-.377.15-.576.47-.651.823-.073.34-.04.736.046 1.136.088.406.238.848.43 1.295a19.697 19.697 0 0 1-1.062 2.227 7.662 7.662 0 0 0-1.482.645c-.37.22-.699.48-.897.787-.21.326-.275.714-.08 1.103z" />
								</svg>
								<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2">{{ data.name }}</span>
							</div>
						</td>
						<td class="px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ checkfile(data.name) }}</span>
						</td>
						<td class="px-1 align-center whitespace-nowrap justify-center text-center">
							<div class="flex justify-center">
								<a :href="BaseUrl(data.src)" target="_blank">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
									</svg>
								</a>
							</div>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
		<div v-if="form.additional_document == 0" tabindex="0" colspan="9" class="outline-none text-xs h-16 bg-white rounded-b align-middle border border-t-0 border-gray-400">
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
						name: this.$t("project.view_page.filename"),
						align: "center",
						filterable: false,
						class: "w-8/12",
					},
					{
						name: this.$t("project.view_page.file_type"),
						align: "center",
						filterable: false,
						class: "w-3/12",
					},
					{
						name: "",
						align: "center",
						filterable: false,
						class: "w-1/12",
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
