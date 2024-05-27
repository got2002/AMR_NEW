<template>
	<section class="pt-2 pb-4">
		<div class="flex justify-between items-center mb-10">
			<div class="text-3xl font-bold">
				{{ $t("project.view_page.page_title") }} 
				#<input type="text" v-model="data.project_id" class="border border-gray-300 outline-none focus:border-green-500 px-2 bg-gray-50"/>
			</div>
			<div class="flex gap-2">
				<UIBackButton @click="$router.push(localePath({ name: 'project-id', params: { id: $route.params.id } }))">{{ $t("button.back") }}</UIBackButton>
				<!-- <nuxt-link :to="localePath({ name: 'project-id', params: { id: $route.params.id } })" class="px-6 py-3 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600">{{ $t("button.back") }}</nuxt-link> -->
				<button @click="deleteProject()" class="px-6 py-3 rounded shadow-sm text-white bg-red-500 hover:bg-red-600 hover:text-theme-white">{{ $t("button.delete") }}</button>
				<button @click="updateProjectAll()" class="px-6 py-3 rounded shadow-sm text-white bg-yellow-500 hover:bg-yellow-600 hover:text-theme-white">{{ $t("button.save") }}</button>
			</div>
		</div>
		<ProjectSkeletonLoad v-if="loading"></ProjectSkeletonLoad>
		<div v-if="!loading" class="flex items-start gap-4">
			<div class="flex flex-col w-1/2 bg-white shadow-md p-4 gap-3 text-sm">
				<UIProjectTextInput :required="true" :label="$t('project.create_page.project_name.th')" v-model="data.project_name.thai" />
				<UIErrorMsg v-if="!$v.data.project_name.thai.required && isSubmitted">{{ $t("project.create_page.form_validation.project_name") }}</UIErrorMsg>
				<UIProjectTextInput :required="true" :label="$t('project.create_page.project_name.en')" v-model="data.project_name.english" />
				<UIErrorMsg v-if="!$v.data.project_name.english.required && isSubmitted">{{ $t("project.create_page.form_validation.project_name") }}</UIErrorMsg>
				
				<UIProjectDropdownInput v-model="data.project_type_by_extens" :options="dropdowns.project_types_ccmgm" :label="$t('project.view_page.knp_rule')" valueAttr="" textAttr="" :required="true" :searchable="true"/>
				<UIErrorMsg v-if="!$v.data.project_type_by_extens.required && isSubmitted">{{ $t("project.create_page.form_validation.knp_rule") }}</UIErrorMsg>

				<UIProjectDropdownInput v-model="data.standard" :options="dropdowns.standards" :label="$t('project.view_page.standard')" :required="true" :searchable="false"/>
				<UIErrorMsg v-if="!$v.data.standard.required && isSubmitted">{{ $t("project.create_page.form_validation.standard") }}</UIErrorMsg>

				<UIProjectDropdownInput :disabled="false" v-model="data.programID" :options="dropdowns.programids" :label="$t('project.view_page.programid')" :searchable="false" :required="true" />
				<UIErrorMsg v-if="!$v.data.programID.required && isSubmitted">{{ $t("project.create_page.form_validation.programid") }}</UIErrorMsg>

				<UIProjectDropdownInput :disabled="false" v-model="data.authorizedUse" :options="dropdowns.autherizeduses" :label="$t('project.view_page.authorizeduse')" :searchable="false" :required="true" />
				<UIErrorMsg v-if="!$v.data.authorizedUse.required && isSubmitted">{{ $t("project.create_page.form_validation.authorizeduse") }}</UIErrorMsg>

				<UIProjectTextInput :disabled="false" v-model="data.reference_link" :label="$t('project.view_page.reference_link')" :required="false" />
				<UIProjectDropdownInput :disabled="false" v-model="data.desAccountNumber" :options="dropdowns.accounts" textAttr="accountName" :label="$t('project.view_page.account')" :required="false" :searchable="true"/>

				<!-- <UIErrorMsg v-if="!$v.data.standard.required && isSubmitted">{{ $t("project.create_page.form_validation.standard") }}</UIErrorMsg> -->

				<div class="space-y-2 mt-5 flex flex-col">
					<div class="text-sm font-bold">{{ $t("project.view_page.project_overview_lang.th") }} <span class="text-red-500">*</span></div>
					<!-- <UILabel :text="$t('project.view_page.project_overview_lang.th')" :required="true"/> -->
					<textarea v-model="data.project_activity" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
					<UIErrorMsg v-if="!$v.data.project_activity.required && isSubmitted">{{ $t("project.create_page.form_validation.project_activity") }}</UIErrorMsg>
				</div>

				<div class="space-y-2 mt-5 flex flex-col">
					<div class="text-sm font-bold">{{ $t("project.view_page.project_overview_lang.en") }} <span class="text-red-500">*</span></div>
					<textarea v-model="data.project_activity_en" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
					<UIErrorMsg v-if="!$v.data.project_activity_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_activity") }}</UIErrorMsg>
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>
				<div class="space-y-2">
					<label class="text-sm font-bold">{{ $t("project.view_page.co_benefit_lang.th") }} </label>
					<ProjectCoBenefitEdit :form="data" />
				</div>

				<div class="space-y-2 mt-5">
					<label class="text-sm font-bold">{{ $t("project.view_page.co_benefit_lang.en") }} </label>
					<ProjectCoBenefitEditEng :form="data" />
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="flex flex-wrap justify-between">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.create_page.project_developer_lang.th") }} <span class="text-red-500">*</span></div>
					</div>
					<input v-model="data.project_developer" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<UIErrorMsg v-if="!$v.data.project_developer.required && isSubmitted">{{ $t("project.create_page.form_validation.project_developer") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.create_page.project_developer_lang.en") }} <span class="text-red-500">*</span></div>
					</div>
					<input v-model="data.project_developer_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<UIErrorMsg v-if="!$v.data.project_developer_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_developer") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.project_owner_lang.th") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input v-model="data.project_owner" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<UIErrorMsg v-if="!$v.data.project_owner.required && isSubmitted">{{ $t("project.create_page.form_validation.project_owner") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.project_owner_lang.en") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input v-model="data.project_owner_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<UIErrorMsg v-if="!$v.data.project_owner_en.required && isSubmitted">{{ $t("project.create_page.form_validation.project_owner") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.external_assessors_lang.th") }}</div>
						</div>
					</div>
					<input v-model="data.external_assessors" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<!-- <UIErrorMsg v-if="!$v.data.external_assessors.required && isSubmitted">{{ $t("project.create_page.form_validation.external_assessors") }}</UIErrorMsg> -->

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.view_page.external_assessors_lang.en") }}</div>
						</div>
					</div>
					<input v-model="data.external_assessors_en" class="w-1/2 text-center border-2 px-3 border-gray-400 bg-gray-50 h-14 flex justify-center items-center" />
				</div>
				<!-- <UIErrorMsg v-if="!$v.data.external_assessors_en.required && isSubmitted">{{ $t("project.create_page.form_validation.external_assessors") }}</UIErrorMsg> -->

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.view_page.registered_date") }} <span class="text-red-500">*</span></div>
					</div>
					<div class="w-1/2 h-14 flex justify-center items-center">
						<DatePicker :lang="$i18n.locale" placeholder="DD MMM YYYY" :formatter="thaiformatter" v-model="data.registration_date" value-type="date" input-class="border-2 border-gray-400 w-full h-14 flex justify-center items-center px-4 text-center"> </DatePicker>
					</div>
				</div>
				<UIErrorMsg v-if="!$v.data.registration_date.required && isSubmitted">{{ $t("project.create_page.form_validation.registered_date") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">{{ $t("project.view_page.credit_period_project") }} <span class="text-red-500">*</span></div>
					</div>
					<div class="w-1/2 h-14 flex justify-center items-center">
						<DatePicker @change="dateChange" range-separator=" - " :formatter="thaiformatter" :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" v-model="periodDate" range value-type="date" input-class="border-2 border-gray-400 w-full h-14 flex justify-center items-center px-4 text-center"></DatePicker>
					</div>
				</div>
				<UIErrorMsg v-if="!$v.data.valid_start.required && isSubmitted">{{ $t("project.create_page.form_validation.credit_period_project") }}</UIErrorMsg>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div v-html="$t('project.view_page.estimated_greenhouse_gases_reduction') + `<span class='text-red-500'> *</span>`" class="text-sm font-bold"></div>
						</div>
					</div>
					<input type="number" v-model="data.approx_co2_reduction_per_year" class="text-center border-2 px-3 border-gray-400 bg-gray-50 w-1/2 h-14 flex justify-center items-center" />
				</div>
				<span v-html="$t('project.create_page.form_validation.estimated_greenhouse_gases_reduction')" class="text-right text-red-500" v-if="!$v.data.approx_co2_reduction_per_year.required && isSubmitted"></span>

				<div class="flex flex-wrap justify-between mt-5">
					<div class="flex flex-col justify-center w-1/2">
						<div class="text-sm font-bold">
							<div class="text-sm font-bold">{{ $t("project.create_page.project_investment") }} <span class="text-red-500">*</span></div>
						</div>
					</div>
					<input type="number" step="any" v-model="data.project_investment" class="text-center border-2 px-3 border-gray-400 bg-gray-50 w-1/2 h-14 flex justify-center items-center" />
				</div>
				<UIErrorMsg v-if="!$v.data.project_investment.required && isSubmitted">{{ $t("project.create_page.form_validation.project_investment") }}</UIErrorMsg>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="space-y-3">
					<div class="text-sm font-bold">{{ $t("project.create_page.reduction_methods.title") }}</div>
					<div class="space-y-2 bg-theme-black-50 p-4">
						<div class="grid grid-cols-2 gap-2" v-for="(method, i) in data.reduction_methods" :key="i">
							<div class="col-span-1">
								<label>{{ $t("project.create_page.reduction_methods.name") }} ({{ i + 1 }}) <span class="text-red-500">*</span></label>
								<input v-model="method.name" class="px-3 py-2 w-full border-2" />
								<UIErrorMsg v-if="!$v.data.reduction_methods.$each[i].name.required && isSubmitted">{{ $t("project.create_page.form_validation.reduction_methods.name") }}</UIErrorMsg>
							</div>
							<div class="col-span-1">
								<label>{{ $t("project.create_page.reduction_methods.document_version") }}</label>
								<div class="flex items-center"><input v-model="method.document_version" class="px-3 py-2 w-full border-2" /> <button @click="removeReductionMethod(i)" v-if="data.reduction_methods.length > 1" class="text-white px-2 py-2 bg-red-500">X</button></div>
							</div>

							<div class="col-span-2">
								<label>{{ $t("project.create_page.reduction_methods.description") }}</label>
								<div class="flex items-center">
									<textarea v-model="method.description" class="px-2 py-3 text-sm border-2 bg-gray-50 w-full" rows="4" />
								</div>
							</div>
						</div>
					</div>

					<div class="flex items-center gap-2 justify-center mt-3">
						<button @click="addReductionMethod()" class="w-1/3 py-3 text-center bg-green-500 rounded shadow-sm text-white cursor-pointer">{{ $t("button.add") }}</button>
					</div>
				</div>
				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.view_page.registered_doc") }}
					<ProjectTablePDFEdit :form="data" />
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.view_page.additional_doc") }}
					<ProjectAdditionalDocument :form="data" />
				</div>
			</div>

			<div class="flex flex-col w-1/2 pl-4 bg-white shadow-md p-4">
				<div class="grid grid-cols-1 gap-2">
					<div class="flex items-center justify-between">
						<div>{{ $t("project.view_page.project_status") }}</div>
						<!-- <div class="flex w-1/3 items-center">
							<select v-model="data.status" class="px-3 py-1.5 w-full border-2 text-center rounded-sm" :class="{ 'bg-red-500 text-white': data.status == 'Cancelled', 'bg-green-500 text-white': data.status == 'Registered', 'bg-gray-500 text-white': data.status == 'Expired' }">
								
								<option class="bg-green-500 text-white" value="Registered">{{ $t("project.view_page.registered") }}</option>
								<option class="bg-red-500 text-white" value="Cancelled">{{ $t("project.view_page.cancelled") }}</option>
								<option class="bg-gray-500 text-white" value="Expired">{{ $t("project.view_page.expired") }}</option>
							</select>
						</div> -->
						<UIStatusOption v-model="data.status" />
					</div>
				</div>
				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="text-sm font-bold mb-2">{{ $t("project.create_page.project_images") }}</div>
				<ProjectImage :form="data" :editMode="true" @saveImage="saveImage" @removeImage="removeImage"></ProjectImage>
				<div class="h-1 border-t-2 border-dashed my-5"></div>
				<ProjectMapEdit :form="data" :height="18" :heightUnit="'rem'" class="flex-grow w-full" :isSubmitted="isSubmitted" />

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="flex flex-col w-full bg-white">
					<div class="mb-4">
						{{ $t("project.view_page.carbon_credits_verified_table") }}
						<ProjectTableCarbonEdit2 :form="data" :edit="true" @reload="getProject()" />
					</div>
					<ProjectApproveCarbon
						v-if="isCertificate"
						:data="data"
						@cancel="isCertificate = false"
						@approved="
							isCertificate = false;
							getProject();
						"
					/>

					<div v-if="!isCertificate" class="flex items-center gap-2 text-white justify-center py-3">
						<button @click="isCertificate = true" class="w-1/3 py-3 text-center bg-green-500 rounded shadow-sm cursor-pointer hover:bg-green-600">{{ $t("button.add") }}</button>
					</div>
					<div class="bg-theme-black-50 p-4 bg-opacity-50 flex gap-3 justify-between rounded border my-4">
						<div v-html="$t('project.view_page.approved_carbon_credits')" class="text-sm font-bold"></div>
						<div class="text-base font-bold mr-3">
							{{ sumCarbon(data.carbon_credit_cert) }}
						</div>
					</div>
				</div>
			</div>
			<!-- <loadingCarbon v-if="!isform" /> -->
		</div>
	</section>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import thaiformatter from "../../../mixins/thaiformatter";
import dropdowns from "../../../mixins/dropdowns";
export default {
	name: "ProjectEdit",
	layout: "DashboardLayout",
	middleware: ["auth"],
	mixins: [thaiformatter, dropdowns],

	asyncData({ params }) {
		const id = params.id;
		return { id };
	},
	data() {
		return {
			lang: "en",
			isCertificate: false,
			data: {},
			isData: false,
			account_id: [],
			edit_approval: {
				text: null,
				value: 0,
			},
			fileArr: [],
			form: {
				amount: 0,
				certified_files: [],
				end_date: null,
				start_date: null,
			},
			dropdowns: {
				project_types: [],
				project_types_ccmgm: [],
				programids: [],
				autherizeduses: [],
				standards: [],
				accounts: [],
			},
			loading: true,
			origin: {},
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
			periodDate: [],
			isSubmitted: false,

			certificate_carbon: {
				start_date: false,
				end_date: false,
				credit: false,
				submitted: false,
			},
		};
	},
	validations() {
		return {
			data: {
				project_name: {
					thai: { required },
					english: { required },
				},
				authorizedUse: { required },
				programID: { required },
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
				project_activity_en: { required },
				// external_assessors: { required },
				// external_assessors_en: { required },
			},
		};
	},
	computed: {
		inputDateFormat() {
			if (this.$i18n.locale === "th") {
				return "DD MMM BBBB";
			}
			return "DD MMM YYYY";
		},
	},
	async mounted() {
		this.dropdowns.project_types_ccmgm = await this.getProjectTypes();
		this.dropdowns.programids = await this.getDropdownProgramID();
		this.dropdowns.autherizeduses = await this.getDropdownAutherizedUse();
		this.dropdowns.standards = await this.getDropdownStandard();
		this.dropdowns.accounts = await this.getAccount();
		await this.getProject();
	},
	methods: {
		// async getDropdownProgramID() {
		// 	const app = this;
		// 	await this.$axios
		// 		.$get(`/api/v1/dropdown/programids`)
		// 		.then((resp) => {
		// 			// console.log(resp);
		// 			app.dropdowns.programids = resp;
		// 			app.isLoading = false;
		// 		})
		// 		.catch((errors) => {
		// 			console.log(errors);
		// 			app.isLoading = false;
		// 		});
		// },
		// async getDropdownAutherizedUse() {
		// 	const app = this;
		// 	await this.$axios
		// 		.$get(`/api/v1/dropdown/authorizeduses`)
		// 		.then((resp) => {
		// 			// console.log(resp);
		// 			app.dropdowns.autherizeduses = resp;
		// 			app.isLoading = false;
		// 		})
		// 		.catch((errors) => {
		// 			console.log(errors);
		// 			app.isLoading = false;
		// 		});
		// },
		// async getDropdownStandard() {
		// 	const app = this;
		// 	await this.$axios
		// 		.$get(`/api/v1/dropdown/projectstandardids`)
		// 		.then((resp) => {
		// 			// console.log(resp);
		// 			app.dropdowns.standards = resp;
		// 			app.isLoading = false;
		// 		})
		// 		.catch((errors) => {
		// 			console.log(errors);
		// 			app.isLoading = false;
		// 		});
		// },
		statusLang(data) {
			if (this.$i18n.locale === "en") {
				return data;
			} else {
				switch (data) {
					case "Registered":
						return "ขึ้นทะเบียนแล้ว";
					case "Cancelled":
						return "ยกเลิกโครงการ";
					default:
						return "ขึ้นทะเบียนแล้ว";
				}
			}
		},
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
			this.data.project_picture.push(img);
			// console.log(this.data.project_picture);
		},
		removeImage(i) {
			this.data.project_picture.splice(i, 1);
		},

		addAddress() {
			this.data.address.push("");
		},
		deleteAddress(i) {
			this.data.address.splice(i, 1);
		},
		addReductionMethod() {
			this.data.reduction_methods.push({
				name: "",
				document_version: "",
				description: "",
			});
		},
		removeReductionMethod(i) {
			this.data.reduction_methods.splice(i, 1);
		},
		// async getTypes() {
		// 	let app = this;
		// 	await this.$axios
		// 		.$get(`/api/v1/dropdown/project-type-by-extends`)
		// 		.then((resp) => {
		// 			// console.log(resp);
		// 			app.dropdowns.project_types_ccmgm = resp;
		// 			app.isLoading = false;
		// 		})
		// 		.catch((errors) => {
		// 			console.log(errors);
		// 			app.isLoading = false;
		// 		});
		// },

		dateChange() {
			[this.data.valid_start, this.data.valid_end] = this.periodDate;
			if (this.periodDate.length === 2 && !this.periodDate.includes(null)) {
				this.data.valid_start = this.$dayjs(this.data.valid_start).format("YYYY-MM-DD");
				this.data.valid_end = this.$dayjs(this.data.valid_end).format("YYYY-MM-DD");
			} else {
				this.data.valid_start = null;
				this.data.valid_end = null;
			}

			// console.log(this.form.valid_start, this.form.valid_end);
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
			this.fileArr.push(process.env.baseUrl + response.src);
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
			this.certificate_carbon.submitted = true;
			if (this.form.start_date === null) {
				this.certificate_carbon.start_date = true;
				app.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.invalid"),
					text: app.$t("project.create_page.form_validation.certificated_carbon_credit.start_date"),
				});
				return;
			}
			if (this.form.end_date === null) {
				this.certificate_carbon.end_date = true;
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
						app.form.start_date = app.$dayjs(app.form.start_date).format("YYYY-MM-DD");
						app.form.end_date = app.$dayjs(app.form.end_date).format("YYYY-MM-DD");
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
								app.certificate_carbon = {
									start_date: false,
									end_date: false,
									credit: false,
									submitted: false,
								};
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: app.$t("sweetalert.successful"),
										confirmButtonColor: "#059669",
									})
									.then(() => {
										app.getProject();
										app.fileArr = [];
										app.form.certified_files = [];
										app.end_date = new Date();
										app.start_date = new Date();
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
		deleteProject() {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#ef4444",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
								</svg>`,

					title: this.$t("alert.title.warning_delete"),
					text: this.$t("alert.text.warning.delete"),
					showCancelButton: true,

					confirmButtonColor: "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("deleting"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$delete(`/api/v1/project/${app.$route.params.id}`)
							.then((resp) => {
								// console.log(resp);
								app.$swal.close();

								// app.form = resp;
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: this.$t("alert.title.success.delete"),
										confirmButtonColor: "#059669",
									})
									.then(() => {
										app.$router.push(app.localePath({ name: "project" }));
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.delete"),
								});
								console.log(err);
							});
					}
				});
		},
		updateProjectAll() {
			const app = this;
			this.isSubmitted = true;
			// console.log("submitted");
			this.$v.$touch();
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
			// app.data.registration_date = app.data.registration_date.substring(0, 10);
			// delete app.data.status;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#f59e0b",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
								</svg>
								`,
					title: this.$t("sweetalert.confirm_correction"),
					text: this.$t("sweetalert.Please_confirm_the_correction"),
					showCancelButton: true,

					confirmButtonColor: "#f59e0b",
					confirmButtonText: this.$t("sweetalert.confirm"),
					cancelButtonText: this.$t("sweetalert.cancel"),
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.form.registration_date = app.$dayjs(app.form.registration_date).format("YYYY-MM-DD");
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$put(`/api/v1/project/${app.$route.params.id}`, app.data)
							.then((resp) => {
								// console.log(resp);
								// app.form = resp;
								app.$swal.close();

								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: app.$t("sweetalert.Correction_succeeded"),
										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										this.$router.push(app.localePath({ name: "project-id", params: { id: app.$route.params.id } }));
									});
								// this.$router.push("/project/" + app.$route.params.id);
							})
							.catch((err) => {
								app.$swal.close();
								console.log(err);
							});
					}
				});
		},

		verification(value) {
			if (this.edit_approval.value === 1 && value === 1) {
				this.edit_approval.value = 0;
				this.data.status = null;
			} else if (this.edit_approval.value === 2 && value === 2) {
				this.edit_approval.value = 0;
				this.data.status = null;
			} else {
				if (value === 1) {
					this.data.status = "Verified";
				} else {
					this.data.status = "Rejected";
				}
			}
		},
		async getProject() {
			const app = this;
			app.loading = true;
			await this.$axios
				.$get(`/api/v1/project/${this.id}`)
				.then((resp) => {
					app.origin = app._.clone(resp);
					app.data = resp;
					// console.log(app.origin);
					if (app.data.reduction_methods.length === 0) {
						app.addReductionMethod();
					}
					app.periodDate = [app.$dayjs(app.data.valid_start).toDate(), app.$dayjs(app.data.valid_end).toDate()];

					app.data.registration_date = app.$dayjs(app.data.registration_date).toDate();
					// app.data.carbon_credit_cert.forEach((element) => {
					// 	element.start_date = element.start_date.substring(0, 10);
					// 	element.end_date = element.end_date.substring(0, 10);
					// });
					// app.data.carbon_credit_cert.sort(function (a, b) {
					// 	return new Date(a.end_date) - new Date(b.end_date);
					// });
					app.isData = true;
					app.loading = false;

					// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
					// this.$router.push("/users/userManagement");
					// setTimeout(this.$toast.clear, 3000);
				})
				.catch((errors) => {
					console.log(errors);
					app.loading = false;

					// this.$toast.error(errors.response.data.errors);
					// setTimeout(this.$toast.clear, 3000);
					app.isData = true;
				});
		},

		sumCarbon(data) {
			let sum = 0;
			const app = this;
			data.forEach((element) => {
				sum += app._.sumBy(element.data, (item) => item.amount);
			});
			return sum?.toLocaleString();
		},
	},
};
</script>
<style scoped>
.style-chooser .vs__search::placeholder,
.style-chooser .vs__dropdown-toggle,
.style-chooser .vs__dropdown-menu {
	background: rgba(249, 250, 251) !important;
	border: none !important;
}
.vs__selected {
	text-align: center !important;
}
.mx-datepicker {
	position: relative;
	display: inline-block;
	width: 100%;
}
</style>
