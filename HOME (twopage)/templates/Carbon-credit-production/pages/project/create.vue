<template>
	<section class="pt-2 pb-4">
		<loadingCarbon v-if="loading"></loadingCarbon>
		<div class="flex justify-between items-center mb-10">
			<h2 class="text-3xl font-bold">{{ $t("project.create_page.page_title") }}</h2>
			<div class="flex gap-2">
				<UIBackButton @click="$router.push(localePath('/project'))">{{ $t("button.cancel") }}</UIBackButton>
				<!-- <nuxt-link :to="localePath('/project')" class="px-6 py-3 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600">{{ $t("button.cancel") }}</nuxt-link> -->
				<button @click="createProject()" class="px-6 py-3 rounded shadow-sm text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 hover:text-theme-white">
					{{ $t("button.create") }}
				</button>
			</div>
		</div>
		<div class="flex items-start gap-4">
			<div class="flex flex-col w-1/2 bg-white shadow-sm rounded p-4 gap-3 text-sm">
				<UIProjectTextInput :required="false" :label="$t('project.create_page.project_id')" v-model="form.project_id" />
				<UIProjectTextInput :required="true" :label="$t('project.create_page.project_name.th')" v-model="form.project_name.thai" />
				<span class="text-right text-red-500" v-if="!$v.form.project_name.thai.required && isSubmitted">{{ $t("project.create_page.form_validation.project_name") }}</span>
				<UIProjectTextInput :required="true" :label="$t('project.create_page.project_name.en')" v-model="form.project_name.english" />
				<span class="text-right text-red-500" v-if="!$v.form.project_name.english.required && isSubmitted">{{ $t("project.create_page.form_validation.project_name") }}</span>
				
				<UIProjectDropdownInput v-model="form.project_type_by_extens" :options="dropdowns.project_types_ccmgm" :label="$t('project.view_page.knp_rule')" valueAttr="" textAttr="" :required="true" :searchable="true"/>
				<UIErrorMsg v-if="!$v.form.project_type_by_extens.required && isSubmitted">{{ $t("project.create_page.form_validation.knp_rule") }}</UIErrorMsg>

				<UIProjectDropdownInput v-model="form.standard" :options="dropdowns.standards" :label="$t('project.view_page.standard')" :required="true" :searchable="false"/>
				<UIErrorMsg v-if="!$v.form.standard.required && isSubmitted">{{ $t("project.create_page.form_validation.standard") }}</UIErrorMsg>

				<UIProjectDropdownInput :disabled="false" v-model="form.programID" :options="dropdowns.programids" :label="$t('project.view_page.programid')" :searchable="false" :required="true" />
				<UIErrorMsg v-if="!$v.form.programID.required && isSubmitted">{{ $t("project.create_page.form_validation.programid") }}</UIErrorMsg>

				<UIProjectDropdownInput :disabled="false" v-model="form.authorizedUse" :options="dropdowns.autherizeduses" :label="$t('project.view_page.authorizeduse')" :searchable="false" :required="true" />
				<UIErrorMsg v-if="!$v.form.authorizedUse.required && isSubmitted">{{ $t("project.create_page.form_validation.authorizeduse") }}</UIErrorMsg>

				<UIProjectTextInput :disabled="false" v-model="form.reference_link" :label="$t('project.view_page.reference_link')" :required="false" />
				<UIProjectDropdownInput :disabled="false" v-model="form.desAccountNumber" :options="dropdowns.accounts" textAttr="accountName" :label="$t('project.view_page.account')" :required="false" :searchable="true"/>

				<div class="space-y-2 mt-5 flex flex-col">
					<div class="text-sm font-bold">{{ $t("project.view_page.project_overview_lang.th") }} <span class="text-red-500">*</span></div>
					<textarea v-model="form.project_activity" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
					<span class="text-right text-red-500" v-if="!$v.form.project_activity.required && isSubmitted">{{ $t("project.create_page.form_validation.project_activity") }}</span>
				</div>

				<div class="space-y-2 mt-5 flex flex-col">
					<div class="text-sm font-bold">{{ $t("project.view_page.project_overview_lang.en") }} <span class="text-red-500">*</span></div>
					<textarea v-model="form.project_activity_en" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
					<span class="text-right text-red-500" v-if="!$v.form.project_activity_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_activity") }}</span>
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="space-y-2">
					<label class="text-sm font-bold">{{ $t("project.view_page.co_benefit_lang.th") }} </label>
					<ProjectCoBenefitEdit :form="form" />
				</div>

				<div class="space-y-2 mt-5">
					<label class="text-sm font-bold">{{ $t("project.view_page.co_benefit_lang.en") }} </label>
					<ProjectCoBenefitEditEng :form="form" />
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="flex justify-between">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.create_page.project_developer_lang.th") }} <span class="text-red-500">*</span></div>
					</div>
					<input v-model="form.project_developer" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.project_developer.required && isSubmitted">{{ $t("project.create_page.form_validation.project_developer") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.create_page.project_developer_lang.en") }} <span class="text-red-500">*</span></div>
					</div>
					<input v-model="form.project_developer_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.project_developer_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_developer") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.project_owner_lang.th") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input v-model="form.project_owner" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.project_owner.required && isSubmitted">{{ $t("project.create_page.form_validation.project_owner") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.project_owner_lang.en") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input v-model="form.project_owner_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.project_owner_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_owner") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.external_assessors_lang.th") }}</div>
						</div>
					</div>
					<input v-model="form.external_assessors" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<!-- <span class="text-right text-red-500" v-if="!$v.form.external_assessors.required && isSubmitted">{{ $t("project.create_page.form_validation.external_assessors") }}</span> -->

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.external_assessors_lang.en") }}</div>
						</div>
					</div>
					<input v-model="form.external_assessors_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<!-- <span class="text-right text-red-500" v-if="!$v.form.external_assessors_en.required && isSubmitted">{{ $t("project.create_page.form_validation.external_assessors") }}</span> -->

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.view_page.registered_date") }} <span class="text-red-500">*</span></div>
					</div>
					<div class="w-1/2 h-14 flex justify-center items-center">
						<DatePicker :lang="$i18n.locale" placeholder="DD MMM YYYY" :formatter="thaiformatter" v-model="form.registration_date" value-type="date" input-class="border-2 border-gray-400 w-full h-14 flex justify-center items-center px-4 text-center"> </DatePicker>
					</div>
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.registration_date.required && isSubmitted">{{ $t("project.create_page.form_validation.registered_date") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.view_page.credit_period_project") }} <span class="text-red-500">*</span></div>
					</div>
					<div class="w-1/2 h-14 flex justify-center items-center">
						<DatePicker @change="dateChange" range-separator=" - " :formatter="thaiformatter" :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" v-model="periodDate" range format="DD MMM YYYY" value-type="date" input-class="border-2 border-gray-400 w-full h-14 flex justify-center items-center px-4 text-center"></DatePicker>
					</div>
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.valid_start.required && isSubmitted">{{ $t("project.create_page.form_validation.credit_period_project") }}</span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold flex">
							<div v-html="$t('project.view_page.estimated_greenhouse_gases_reduction') + `<span class='text-red-500'> *</span>`" class="text-sm font-bold"></div>
						</div>
					</div>
					<input type="number" v-model="form.approx_co2_reduction_per_year" class="text-center border-2 px-3 border-gray-400 bg-gray-50 w-1/2 h-14 flex justify-center items-center" />
				</div>
				<span v-html="$t('project.create_page.form_validation.estimated_greenhouse_gases_reduction')" class="text-right text-red-500" v-if="!$v.form.approx_co2_reduction_per_year.required && isSubmitted"></span>

				<div class="flex justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.create_page.project_investment") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input type="number" step="any" v-model="form.project_investment" class="text-center border-2 px-3 border-gray-400 bg-gray-50 w-1/2 h-14 flex justify-center items-center" />
				</div>
				<span class="text-right text-red-500" v-if="!$v.form.project_investment.required && isSubmitted">{{ $t("project.create_page.form_validation.project_investment") }}</span>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="space-y-3">
					<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.title") }}</div>
					<div class="space-y-2 bg-theme-black-50 p-4">
						<div class="grid grid-cols-2 gap-2" v-for="(method, i) in form.reduction_methods" :key="i">
							<div class="col-span-1">
								<label>{{ $t("project.create_page.reduction_methods.name") }} ({{ i + 1 }}) <span class="text-red-500">*</span></label>
								<input v-model="method.name" class="px-3 py-2 w-full border-2" />
								<span class="text-right text-red-500" v-if="!$v.form.reduction_methods.$each[i].name.required && isSubmitted">{{ $t("project.create_page.form_validation.reduction_methods.name") }}</span>
							</div>
							<div class="col-span-1">
								<label>{{ $t("project.create_page.reduction_methods.document_version") }}</label>
								<div class="flex items-center">
									<input v-model="method.document_version" class="px-3 py-2 w-full border-2" />
									<button @click="removeReductionMethod(i)" v-if="form.reduction_methods.length > 1" class="text-white px-2 py-2 bg-red-500">X</button>
								</div>
							</div>
							<!-- <div class="col-span-1">
								<label>{{ $t("project.create_page.reduction_methods.description") }}</label>
								<div class="flex items-center">
									<input v-model="method.description" class="px-3 py-2 w-full border-2" />
									
								</div>
							</div> -->
							<div class="col-span-2">
								<label>{{ $t("project.create_page.reduction_methods.description") }}</label>
								<div class="flex items-center">
									<textarea v-model="method.description" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
								</div>
							</div>
						</div>
					</div>

					<div class="flex items-center gap-2 text-white justify-center mt-3">
						<button @click="addReductionMethod()" class="w-1/3 py-3 text-center bg-green-500 cursor-pointer">{{ $t("button.add") }}</button>
					</div>
				</div>
			</div>

			<div class="flex flex-col w-1/2 pl-4 shadow-sm rounded bg-white p-4">
				<div class="text-sm font-bold mb-2">{{ $t("project.create_page.project_images") }}</div>
				<ProjectImage :form="form" :editMode="true" @saveImage="saveImage" @removeImage="removeImage"></ProjectImage>
				<div class="h-1 border-t-2 border-dashed my-5"></div>
				<ProjectMapCreate :form="form" :height="18" :heightUnit="'rem'" class="flex-grow w-full" :isSubmitted="isSubmitted" />

				<!-- <div class="h-1 border-t-2 border-dashed my-5"></div>
				<div class="">
					<div class="text-sm font-bold mb-2">{{ $t("project.create_page.address.title") }} <span class="text-red-500">*</span></div>
					<div class="p-4 bg-theme-black-50">
						<ProjectAddress :isSubmitted="isSubmitted" :form="form" @deleteAddress="deleteAddress"></ProjectAddress>
					</div>

					<div class="flex items-center gap-2 text-white justify-center py-3">
						<button @click="addAddress()" class="w-1/3 py-3 text-center bg-green-500 cursor-pointer">{{ $t("button.add") }}</button>
					</div>
				</div> -->

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.view_page.registered_doc") }}
					<ProjectTablePDFEdit :form="form" />
				</div>

				<!-- <div class="mt-5">
					{{ $t("project.view_page.carbon_credits_verified_table") }}
					<ProjectTableCarbonEdit :form="data" :edit="true" />
				</div> -->

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.view_page.additional_doc") }}
					<ProjectAdditionalDocument :form="form" />
				</div>

				<div class="mt-5">
					{{ $t("project.view_page.carbon_credits_verified_table") }}
				</div>
				<div :key="index" class="flex flex-col justify-center items-center w-full col-span-2 mb-5" v-for="(carbon, index) in form.carbon_credit_cert">
					<ProjectDropzone :carbon="carbon" :index="index" @deleteCarbon="deleteCarbon" />
				</div>
				<div class="flex items-center gap-2 text-white justify-center py-3">
					<label for="approve" class="w-1/3 py-3 text-center bg-green-500 rounded shadow-sm cursor-pointer" :class="{ 'bg-green-700': edit_approval.value == 1 }">{{ $t("button.add") }}</label>
					<input @click="addCarbon()" type="button" id="approve" class="hidden" />
				</div>
			</div>
			<!-- <loadingCarbon v-if="!isform" /> -->
		</div>
	</section>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import Dropzone from "nuxt-dropzone";
import "nuxt-dropzone/dropzone.css";
import thaiformatter from "../../mixins/thaiformatter";
import dropdowns from "../../mixins/dropdowns";
export default {
	name: "DocumentPage",
	layout: "DashboardLayout",
	middleware: ["auth"],
	components: {
		// Dropzone,
	},
	asyncData({ params }) {
		const id = params.id;
		return { id };
	},
	mixins: [thaiformatter, dropdowns],
	data() {
		return {
			data: {},
			isData: false,
			edit_approval: {
				text: null,
				value: 0,
			},
			dropdowns: {
				project_types: [],
				project_types_ccmgm: [],
				programids: [],
				autherizeduses: [],
				standards: [],
				accounts:[]
			},
			fileArr: [],
			periodDate: [],
			form: {
				project_name: {
					thai: "",
					english: "",
				},
				co_benefit: {
					environment: "",
					society: "",
					economy: "",
				},
				reference_link:'',
				desAccountNumber:null,


				authorizedUse: "",
				programID: "",
				standard: "Standard T-VER",
				project_id: "",
				address: [],
				address_en: [],
				project_picture: [],
				reduction_methods: [
					{
						name: "",
						document_version: "",
						description: "",
					},
				],
				area: null,
				registration_date: "",
				valid_start: "",
				valid_end: "",
				carbon_credit_wallet: 0,
				status: "",
				project_investment: null,

				project_developer: "",
				project_owner: "",
				// project_type: "",
				project_type_by_extens: "",
				project_activity: "",
				approx_co2_reduction_per_year: null,
				registration_files: [],
				additional_document: [],
				carbon_credit_cert: [],
				location: {
					type: "FeatureCollection",
					features: [],
				},
				owner_id: "633bc00dc01eb36cc0d50f3a",
				project_developer_en: "",
				project_owner_en: "",
				project_activity_en: "",
				external_assessors: "",
				external_assessors_en: "",
				co_benefit_en: {
					environment: "",
					society: "",
					economy: "",
				},
			},
			loading: false,
			origin: {},
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
			isSubmitted: false,
		};
	},

	validations() {
		return {
			form: {
				authorizedUse: { required },
				programID: { required },
				project_name: {
					thai: { required },
					english: { required },
				},
				// co_benefit: {
				// 	environment: {required},
				// 	society: "",
				// 	economy: "",
				// },
				// project_id: "",
				address: {
					$each: { required },
				},
				address_en: {
					$each: { required },
				},
				reduction_methods: {
					$each: {
						name: { required },
					},
				},

				registration_date: { required },
				valid_start: { required },
				valid_end: { required },
				standard: { required },

				project_investment: { required },

				project_developer: { required },
				project_owner: { required },
				// project_type: { required },
				project_type_by_extens: { required },
				project_activity: { required },
				approx_co2_reduction_per_year: { required },
				project_developer_en: { required },
				project_owner_en: { required },
				// external_assessors: { required },
				// external_assessors_en: { required },

				project_activity_en: { required },
			},
		};
	},

	async mounted() {
		// this.dropdowns.project_types_ccmgm = await this.getProjectTypesBBR();
		this.dropdowns.project_types_ccmgm = await this.getProjectTypes();
		this.dropdowns.programids = await this.getDropdownProgramID();
		this.dropdowns.autherizeduses = await this.getDropdownAutherizedUse();
		this.dropdowns.standards = await this.getDropdownStandard();
		this.dropdowns.accounts = await this.getAccount()
	},
	methods: {
		ccmgm(data) {
			if (this.$i18n.locale === "th") {
				return data;
			} else {
				switch (data) {
					case "พลังงานหมุนเวียนหรือพลังงานที่ใช้ทดแทนเชื้อเพลิงฟอสซิล":
						return "Renewable energy or fossil fuel replacement";
					case "การเพิ่มประสิทธิภาพการผลิตไฟฟ้าและการผลิตความร้อน":
						return "Improvement of the efficiency of electricity and heat generation";
					case "การใช้ระบบขนส่งสาธารณะ":
						return "Use of public transportation system";
					case "การใช้ยานพาหนะไฟฟ้า":
						return "Use of electric vehicle";
					case "การเพิ่มประสิทธิภาพเครื่องยนต์":
						return "Improvement of the efficiency of engine";
					case "การเพิ่มประสิทธิภาพการใช้พลังงานในอาคารและโรงงาน และในครัวเรือน":
						return "Improvement of the efficiency of energy consumption in building and factory and in household";
					case "การปรับเปลี่ยนสารทำความเย็นธรรมชาติ":
						return "Use of natural refrigerant";
					case "การใช้วัสดุทดแทนปูนเม็ด":
						return "Use of clinker substitute";
					case "การจัดการขยะมูลฝอย":
						return "Solid waste management";
					case "การจัดการน้ำเสียชุมชน":
						return "Domestic wastewater management";
					case "การนำก๊าซมีเทนกลับมาใช้ประโยชน์":
						return "Methane recovery and utilization";
					case "การจัดการน้ำเสียอุตสาหกรรม":
						return "Industrial wastewater management";
					case "การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร":
						return "Reduction, absorption and removal of greenhouse gases from the forestry and agriculture sectors";
					case "การดักจับ กักเก็บ และ/หรือใช้ประโยชน์จากก๊าซเรือนกระจก":
						return "Capture, storage, and/or utilization of greenhouse gas";
					default:
						return "Other project specified by the Board of Directors of TGO";
				}
			}
		},
		saveImage(img) {
			// console.log(img);
			this.form.project_picture.push(img);
			// console.log(this.form.project_picture);
		},
		removeImage(i) {
			this.form.project_picture.splice(i, 1);
		},
		dateChange() {
			[this.form.valid_start, this.form.valid_end] = this.periodDate;
			if (this.periodDate.length === 2 && !this.periodDate.includes(null)) {
				this.form.valid_start = this.$dayjs(this.form.valid_start).format("YYYY-MM-DD");
				this.form.valid_end = this.$dayjs(this.form.valid_end).format("YYYY-MM-DD");
			} else {
				this.form.valid_start = null;
				this.form.valid_end = null;
			}
			// console.log(this.form.valid_start, this.form.valid_end);
		},
		// addAddress() {
		// 	this.form.address.push("");
		// },
		deleteAddress(i) {
			this.form.address.splice(i, 1);
		},
		addReductionMethod() {
			this.form.reduction_methods.push({
				name: "",
				document_version: "",
				description: "",
			});
		},
		removeReductionMethod(i) {
			this.form.reduction_methods.splice(i, 1);
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
			// this.form.certified_files.push(response);
			this.fileArr.push(process.env.baseUrl + response.src);
			// this.$refs.dropDocument9.removeAllFiles();
		},

		createProject() {
			const app = this;
			this.isSubmitted = true;
			// console.log("submitted");
			this.$v.$touch();
			// console.log(app.form);
			// console.log("submitted & touch");
			if (this.$v.$invalid) {
				// console.log("submitted & invalid");
				this.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.complete_information"),
					text: this.$t("sweetalert.complete_information_text"),
				});

				return;
			}
			// console.log("submitted & validation");

			this.$swal
				.fire({
					icon: "info",
					iconColor: "#4CA365",
					title: this.$t("sweetalert.confirm_creation"),
					text: this.$t("sweetalert.Please_confirm_the_creation"),
					showCancelButton: true,

					confirmButtonColor: "#4CA365",
					confirmButtonText: this.$t("sweetalert.confirm"),
					cancelButtonText: this.$t("sweetalert.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.loading = true;
						app.form.registration_date = app.$dayjs(app.form.registration_date).format("YYYY-MM-DD");
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/project/`, app.form)
							.then((resp) => {
								// console.log(resp);
								// app.form = resp;

								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: app.$t("sweetalert.creation_success"),
										confirmButtonColor: "#059669",
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										this.$router.push(app.localePath({ name: "project-id", params: { id: resp.data._id } }));
									});
							})
							.catch((err) => {
								app.$swal.close();

								console.log(err);
							});
					}
				});
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
				reader.onload = function (e) {
					app.fileArr.push(e.target.result);
				};

				reader.readAsDataURL(fileItem);
			}
		},
		removeImg(idx) {
			this.fileArr.splice(idx, 1);
			// this.form.certified_files.splice(idx, 1);
		},
		addCarbon() {
			// this.fileArr.splice(idx, 1);
			// this.fileArr.push({
			// 	start_date: "",
			// 	end_date: "",
			// 	amount: 0,
			// 	certified_files: [],
			// });
			this.form.carbon_credit_cert.push({
				start_date: "",
				end_date: "",
				amount: 0,
				certified_files: [],
			});
		},
		deleteCarbon(i) {
			this.form.carbon_credit_cert.splice(i, 1);
		},
	},
};
</script>

<style>
.mx-datepicker {
	position: relative;
	display: inline-block;
	width: 100%;
}
</style>
