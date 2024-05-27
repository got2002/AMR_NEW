<template>
	<div class="p-4 border">
		<div class="flex flex-col justify-center items-center w-full col-span-2 mb-2">
			<div class="grid grid-cols-12 gap-2">
				<div class="col-span-8">
					<UILabel :text="$t('project.view_page.start_date') + '-' + $t('project.view_page.end_date')" :required="true"/>
					<DatePicker :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date') + '-' + $t('project.view_page.end_date')" v-model="form.certifiedDate" :formatter="thaiformatter" range value-type="date" input-class="w-full py-2 px-2 border border-gray-300 text-center rounded bg-gray-50"> </DatePicker>
                    <UIErrorMsg v-if="checkInvalidDate && submitted">{{ $t("project.create_page.form_validation.certificated_carbon_credit.certification_date") }}</UIErrorMsg>
                   
                </div>
				<!-- <div class="text-sm mr-2">
					<label>{{ $t("project.view_page.start_date") }} <span class="text-red-500">*</span></label>

					<div class="w-full border-2 h-8">
						<DatePicker :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date')" v-model="form.start_date" :formatter="thaiformatter" value-type="date" input-class=" ml-1 p-1 px-2 text-center"> </DatePicker>
					</div>
					<span class="text-right text-red-500 text-xs" v-if="certificate_carbon.start_date && certificate_carbon.submitted">{{ $t("project.create_page.form_validation.certificated_carbon_credit.start_date") }}</span>
				</div>
				<div class="text-sm mr-2">
					<label>{{ $t("project.view_page.end_date") }} <span class="text-red-500">*</span></label>
					
					<div class="w-full border-2 h-8">
						<DatePicker :lang="$i18n.locale" :placeholder="$t('project.view_page.end_date')" v-model="form.end_date" :formatter="thaiformatter" value-type="date" input-class=" ml-1 p-1 px-2 text-center"> </DatePicker>
					</div>
					<span class="text-right text-red-500 text-xs" v-if="certificate_carbon.end_date && certificate_carbon.submitted">{{ $t("project.create_page.form_validation.certificated_carbon_credit.end_date") }}</span>
				</div> -->
				<div class="col-span-4">
					
					<UILabel :text="$t('project.view_page.amount') " :required="true"/>
					<UINumberInput v-model.number="form.amount" class="text-center"/>
					
				</div>
			</div>
		</div>
		<UILabel :text="$t('openAccount.document')"/>
		<dropzone id="dropDocument2" ref="dropDocument2" :options="dropzoneOptions" :useCustomSlot="true" @vdropzone-success="uploadSuccess" class="cursor-pointer w-full h-full border-dashed border-1 border-primary-dark">
			<label for="dropDocument2" class="">
				<div class="flex flex-col justify-center items-center py-2 border border-dashed border-gray-400 rounded mb-2">
					<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
						<span class="font-semibold">{{ $t("project.view_page.Click_to_select_a_file") }}</span> {{ $t("project.view_page.or_drag") }}
					</p>
					<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, PDF or GIF</p>
				</div>
			</label>
		</dropzone>
        <div class="space-y-2">
			<div class="w-full py-2 bg-gray-100 hover:bg-gray-200 px-2 flex items-center justify-between rounded-sm" v-for="(file, idx) in form.certified_files" :key="idx">
				<div v-if="checkfile(file.src) === 'pdf'" @click="openPDF(file.src)" class="text-sm hover:underline cursor-pointer">{{ file.name }}</div>
				<div v-else @click="showImage(file.src)" class="text-sm hover:underline cursor-pointer">{{ file.name }}</div>
				<button @click="removeFile(idx)" class="">
					<IconXMark />
				</button>
			</div>
			<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>
			<client-only placeholder="loading...">
				<EasyLightBox :imgs="[imgURL]" :visible="visible" @hide="visible = false"> </EasyLightBox>
			</client-only>
		</div>

		<div class="flex items-center justify-center gap-4 mt-5">
			<button @click="$emit('cancel')" class="w-20 py-2 bg-gray-300 rounded shadow-sm ">{{ $t("button.cancel") }}</button>
			<button @click="approvalProject()" class="w-20 py-2 bg-tgo-teal-500 rounded shadow-sm text-white">{{ $t("button.save") }}</button>
		</div>
	</div>
</template>

<script>
import Dropzone from "nuxt-dropzone";
import "nuxt-dropzone/dropzone.css";
import EasyLightBox from "vue-easy-lightbox";
import thaiformatter from "../../mixins/thaiformatter";
export default {
	props: ["data"],
	mixins: [thaiformatter],
	components: {
		Dropzone,
		EasyLightBox,
	},
	computed: {
		previewImg() {
			let arr = [];
			arr = this._.map(this.form.project_picture, (item) => {
				const newUrl = process.env.baseUrl + item.src;
				return {
					src: newUrl,
					name: item.name,
				};
			});
			return arr;
		},
        checkInvalidDate(){
            if(this.form.certifiedDate.length === 2){
                if(this.form.certifiedDate.includes(null)){
                    return true
                }
                else return false
            }
            else{
                return true
            }
        }
	},
	data: () => {
		return {
			pdfURL: "",
			pdfModal: false,
			imgURL: "",
			visible: false,
            submitted:false,
			form: {
				amount: 0,
				certified_files: [],
				
				certifiedDate: [],
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
	methods: {
		showImage(src) {
			this.imgURL = process.env.baseUrl + src;
			this.visible = true;
		},
		removeFile(idx) {
			this.form.certified_files.splice(idx, 1);
		},
		openPDF(src) {
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},
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
			this.form.certified_files.push(response);
			// this.fileArr.push(process.env.baseUrl + response.src);
			this.$refs.dropDocument2.removeAllFiles();
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},

		approvalProject() {
			const app = this;
			this.submitted = true
			if (this.checkInvalidDate) {
				
				app.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.invalid"),
					text: app.$t("project.create_page.form_validation.certificated_carbon_credit.start_date"),
				});
				return;
			}
			if (this.checkInvalidDate) {
				
				app.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.invalid"),
					text: app.$t("project.create_page.form_validation.certificated_carbon_credit.end_date"),
				});
				return;
			}
			app.$swal
				.fire({
					icon: "info",
					iconColor: "#00b0d8",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
								</svg>
								`,
					title: this.$t("sweetalert.confirm_certificate.title"),
					text: this.$t("sweetalert.confirm_certificate.text"),
					showCancelButton: true,

					confirmButtonColor: "#00b0d8",
					confirmButtonText: this.$t("sweetalert.confirm"),
					cancelButtonText: this.$t("sweetalert.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						// app.loading = true;
						app.form.sub_status = "Certified";
						app.form.start_date = app.$dayjs(app.form.certifiedDate[0]).format("YYYY-MM-DD");
						app.form.end_date = app.$dayjs(app.form.certifiedDate[1]).format("YYYY-MM-DD");
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("loading"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/project/approval/${app.$route.params.id}`, app.form)
							.then((resp) => {
								// app.loading = false;
								app.$swal.close();
								
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: app.$t("sweetalert.successful"),
										confirmButtonColor: "#059669",
									})
									.then(() => {
										app.$emit('approved');
										
										app.form.certified_files = [];
										app.certifiedDate = []
										app.amount = 0;
									});
							})
							.catch((err) => {
								// app.loading = false;
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: app.$t("sweetalert.error"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>

<style>
</style>