<template>
	<div>
		<div class="flex w-full justify-between items-center mb-3">
			<div class="text-sm mr-2">
				<label>{{ $t("project.view_page.start_date") }}</label>

				<div class="w-full border-2 h-8">
					<DatePicker lang="th" placeholder="DD MMM YYYY" v-model="carbon.start_date" format="DD MMM YYYY" value-type="YYYY-MM-DD" input-class=" ml-1 p-1 px-2 text-center"> </DatePicker>
				</div>
			</div>
			<div class="text-sm mr-2">
				<label>{{ $t("project.view_page.end_date") }}</label>
				<!-- <input type="date" class="border-2 ml-1 p-1" v-model="form.end_date" /> -->
				<div class="w-full border-2 h-8">
					<DatePicker lang="th" placeholder="DD MMM YYYY" v-model="carbon.end_date" format="DD MMM YYYY" value-type="YYYY-MM-DD" input-class=" ml-1 p-1 px-2 text-center"> </DatePicker>
				</div>
			</div>
			<div class="text-sm mr-2">
				<label>{{ $t("project.view_page.amount") }}</label>
				<div class="w-full border-2">
					<input type="number" v-model.number="carbon.amount" class="ml-1 p-1 px-2 text-center" />
				</div>
			</div>
			<div @click="$emit('deleteCarbon', index)" class="rounded-full bg-gray-200 border shadow-sm">
				<font-awesome-icon icon="fas fa-times"></font-awesome-icon>
			</div>
		</div>
		<dropzone id="dropDocument9" ref="dropDocument9" :options="dropzoneOptions" :useCustomSlot="true" @vdropzone-success="uploadSuccess" class="cursor-pointer w-full h-full border-dashed border-1 border-primary-dark">
			<label for="dropDocument9" class="flex flex-col z-0 justify-center items-center h-auto bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
				<div class="flex flex-col justify-center items-center pt-5 pb-6" v-if="carbon.certified_files.length == 0">
					<svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
					<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
						<span class="font-semibold">{{ $t("project.view_page.Click_to_select_a_file") }}</span> {{ $t("project.view_page.or_drag") }}
					</p>
					<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, PDF or GIF</p>
				</div>
				<div class="w-full grid grid-cols-4 gap-4 items-center justify-center p-5" v-if="carbon.certified_files.length > 0">
					<div class="col-span-1 bg-white shadow-sm border rounded-md relative" v-for="(img, idx) in carbon.certified_files" :key="idx">
						<div @click="removeImg(idx)" class="absolute z-50 -right-3 -top-3 p-2 rounded-full bg-gray-200 border shadow-sm">
							<font-awesome-icon icon="fas fa-times"></font-awesome-icon>
						</div>
						<div v-if="checkfile(img.name) == 'pdf'">
							<div class="w-full h-36 rounded-md flex">
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="bg-red-500" class="bi bi-file-earmark-pdf-fill" viewBox="0 0 16 16">
									<path d="M5.523 12.424c.14-.082.293-.162.459-.238a7.878 7.878 0 0 1-.45.606c-.28.337-.498.516-.635.572a.266.266 0 0 1-.035.012.282.282 0 0 1-.026-.044c-.056-.11-.054-.216.04-.36.106-.165.319-.354.647-.548zm2.455-1.647c-.119.025-.237.05-.356.078a21.148 21.148 0 0 0 .5-1.05 12.045 12.045 0 0 0 .51.858c-.217.032-.436.07-.654.114zm2.525.939a3.881 3.881 0 0 1-.435-.41c.228.005.434.022.612.054.317.057.466.147.518.209a.095.095 0 0 1 .026.064.436.436 0 0 1-.06.2.307.307 0 0 1-.094.124.107.107 0 0 1-.069.015c-.09-.003-.258-.066-.498-.256zM8.278 6.97c-.04.244-.108.524-.2.829a4.86 4.86 0 0 1-.089-.346c-.076-.353-.087-.63-.046-.822.038-.177.11-.248.196-.283a.517.517 0 0 1 .145-.04c.013.03.028.092.032.198.005.122-.007.277-.038.465z" />
									<path fill-rule="evenodd" d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2zm5.5 1.5v2a1 1 0 0 0 1 1h2l-3-3zM4.165 13.668c.09.18.23.343.438.419.207.075.412.04.58-.03.318-.13.635-.436.926-.786.333-.401.683-.927 1.021-1.51a11.651 11.651 0 0 1 1.997-.406c.3.383.61.713.91.95.28.22.603.403.934.417a.856.856 0 0 0 .51-.138c.155-.101.27-.247.354-.416.09-.181.145-.37.138-.563a.844.844 0 0 0-.2-.518c-.226-.27-.596-.4-.96-.465a5.76 5.76 0 0 0-1.335-.05 10.954 10.954 0 0 1-.98-1.686c.25-.66.437-1.284.52-1.794.036-.218.055-.426.048-.614a1.238 1.238 0 0 0-.127-.538.7.7 0 0 0-.477-.365c-.202-.043-.41 0-.601.077-.377.15-.576.47-.651.823-.073.34-.04.736.046 1.136.088.406.238.848.43 1.295a19.697 19.697 0 0 1-1.062 2.227 7.662 7.662 0 0 0-1.482.645c-.37.22-.699.48-.897.787-.21.326-.275.714-.08 1.103z" />
								</svg>
								{{ filename(img.name) }}
							</div>
						</div>
						<div v-else>
							<img :src="baseUrl + img.src" class="w-full h-36 rounded-md" />
						</div>
					</div>
				</div>
			</label>
		</dropzone>
	</div>
</template>
<script>
import Dropzone from "nuxt-dropzone";
import "nuxt-dropzone/dropzone.css";
export default {
	props: ["carbon", "index"],
	data() {
		return {
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
		};
	},
	components: {
		Dropzone,
	},
	computed: {
        baseUrl:function(){
            return process.env.baseUrl
        }
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
		filename(filename) {
			let parts = filename.split("/");
			parts = parts[parts.length - 1];
			return parts.toLowerCase();
		},
		uploadSuccess(file, response) {
			this.carbon.certified_files.push(response);
			this.$refs.dropDocument9.removeAllFiles();
		},
		removeImg(idx) {
			this.carbon.certified_files.splice(idx, 1);
		},
	},
};
</script>
