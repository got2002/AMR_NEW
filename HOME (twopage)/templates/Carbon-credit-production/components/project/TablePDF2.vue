<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-4">
		<table class="items-center w-full space-y-6 border border-theme-black-300">
			<thead>
				<tr>
					<template v-for="(item, idx) in table.head">
						<ApiHeadSlotWhite :class="item.class" :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody v-if="pdf[number] != undefined" class="bg-white border border-theme-black-300">
				<template v-for="(data, index) in form.certified_files">
					<tr tabindex="0" :key="index" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300">
						<td class="border-t-0 px-10 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<div class="w-full flex items-center">
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="bg-red-500" class="bi bi-file-earmark-pdf-fill" viewBox="0 0 16 16">
									<path d="M5.523 12.424c.14-.082.293-.162.459-.238a7.878 7.878 0 0 1-.45.606c-.28.337-.498.516-.635.572a.266.266 0 0 1-.035.012.282.282 0 0 1-.026-.044c-.056-.11-.054-.216.04-.36.106-.165.319-.354.647-.548zm2.455-1.647c-.119.025-.237.05-.356.078a21.148 21.148 0 0 0 .5-1.05 12.045 12.045 0 0 0 .51.858c-.217.032-.436.07-.654.114zm2.525.939a3.881 3.881 0 0 1-.435-.41c.228.005.434.022.612.054.317.057.466.147.518.209a.095.095 0 0 1 .026.064.436.436 0 0 1-.06.2.307.307 0 0 1-.094.124.107.107 0 0 1-.069.015c-.09-.003-.258-.066-.498-.256zM8.278 6.97c-.04.244-.108.524-.2.829a4.86 4.86 0 0 1-.089-.346c-.076-.353-.087-.63-.046-.822.038-.177.11-.248.196-.283a.517.517 0 0 1 .145-.04c.013.03.028.092.032.198.005.122-.007.277-.038.465z" />
									<path fill-rule="evenodd" d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2zm5.5 1.5v2a1 1 0 0 0 1 1h2l-3-3zM4.165 13.668c.09.18.23.343.438.419.207.075.412.04.58-.03.318-.13.635-.436.926-.786.333-.401.683-.927 1.021-1.51a11.651 11.651 0 0 1 1.997-.406c.3.383.61.713.91.95.28.22.603.403.934.417a.856.856 0 0 0 .51-.138c.155-.101.27-.247.354-.416.09-.181.145-.37.138-.563a.844.844 0 0 0-.2-.518c-.226-.27-.596-.4-.96-.465a5.76 5.76 0 0 0-1.335-.05 10.954 10.954 0 0 1-.98-1.686c.25-.66.437-1.284.52-1.794.036-.218.055-.426.048-.614a1.238 1.238 0 0 0-.127-.538.7.7 0 0 0-.477-.365c-.202-.043-.41 0-.601.077-.377.15-.576.47-.651.823-.073.34-.04.736.046 1.136.088.406.238.848.43 1.295a19.697 19.697 0 0 1-1.062 2.227 7.662 7.662 0 0 0-1.482.645c-.37.22-.699.48-.897.787-.21.326-.275.714-.08 1.103z" />
								</svg>
								<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 truncate w-28 md:w-32 lg:w-48 xl:w-48 2xl:w-96">{{ data.name }}</span>
							</div>
						</td>
						<!-- <td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">PDF</span>
						</td> -->
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ checkfile(data.name) }}</span>
						</td>
						<td class="border-t-0 px-10 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<div class="flex justify-center">
								<a :href="BaseUrl(data.src)" target="_blank">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
									</svg>
								</a>
								<button v-if="edit" @click="deletePDF(index)" target="_blank" class="ml-3">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
									</svg>
								</button>
							</div>
						</td>
					</tr>
				</template>
			</tbody>
			<div v-else class="flex justify-center col-span-3">{{ $t("alert.no_data") }}</div>
		</table>
		<!-- <div v-if="edit" class="flex justify-center items-center mt-3">
			<label for="dropzone-file-3" class="flex flex-col z-0 justify-center items-center w-3/4 h-64 bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
				<div class="flex flex-col justify-center items-center pt-5 pb-6">
					<svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
					<p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">{{$t('project.view_page.Click_to_select_a_file')}}</span> {{$t('project.view_page.or_drag')}}</p>
					<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, PDF or GIF</p>
				</div>
				<input id="dropzone-file-3" type="file" accept="image/png, image/gif, image/jpeg, image/svg, application/pdf" class="hidden" @change="uploadImages" multiple />
			</label>
		</div> -->
		<div v-if="edit" class="flex justify-center items-center mt-3 w-full">
			<dropzone id="dropDocument3" ref="dropDocument3" :options="dropzoneOptions" :useCustomSlot="true" @vdropzone-success="uploadSuccess" class="cursor-pointer w-full h-full border-dashed border-1 border-primary-dark">
				<label for="dropDocument3" class="flex flex-col z-0 justify-center items-center h-auto bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
					<div class="flex flex-col justify-center items-center pt-5 pb-6">
						<svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
						<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
							<span class="font-semibold">{{ $t("project.view_page.Click_to_select_a_file") }}</span> {{ $t("project.view_page.or_drag") }}
						</p>
						<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, PDF or GIF</p>
					</div>
				</label>
			</dropzone>
		</div>
	</div>
</template>

<script>
import Dropzone from "nuxt-dropzone";
import "nuxt-dropzone/dropzone.css";
export default {
	props: ["number", "form", "edit"],
	components: {
		Dropzone,
	},
	data() {
		return {
			isData: false,
			pdf: [
				["F-MR_TOP SPP.pdf", "F-Verification Report_TOP SPP.pdf"],
				["F-Monitoring Report_TOP SPP.pdf", "F-Verification Report_TOP SPP (1).pdf"],
				["F-MR_TOP SPP (1).pdf", "F-Verification Report_TOP SPP (2).pdf"],
			],
			table: {
				head: [
					{
						name: this.$t("project.view_page.filename"),
						align: "center",
						filterable: false,
						class:'w-8/12'
					},
					{
						name: this.$t("project.view_page.file_type"),
						align: "center",
						filterable: false,
						class:'w-3/12'
					},
					{
						name: "",
						align: "center",
						filterable: false,
						class:'w-1/12'
					},
				],
			},
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
		};
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		// console.log(this.form);
	},
	methods: {
		checkfile(filename) {
			let parts = filename.split(".");
			parts = parts[parts.length - 1];
			return parts.toLowerCase();
		},
		uploadSuccess(file, response) {
			this.form.certified_files.push(response);
			this.$refs.dropDocument3.removeAllFiles();
		},
		deletePDF(index) {
			this.form.certified_files.splice(index, 1);
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
			console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum;
		},
		async uploadImages(input) {
			const app = this;
			const fileLength = input.target.files.length;
			for (let i = 0; i < fileLength; i++) {
				const formData = new FormData();
				const fileItem = input.target.files[i];
				// console.log(fileItem);
				formData.append("file", fileItem);
				await this.$axios
					.$post(`/api/v1/form/upload`, formData)
					.then((resp) => {
						app.form.certified_files.push(resp);
						// console.log(app.form.certified_files);
					})
					.catch((err) => {
						console.log(err);
					});
				const reader = new FileReader();

				reader.readAsDataURL(fileItem);
			}
		},
	},
};
</script>