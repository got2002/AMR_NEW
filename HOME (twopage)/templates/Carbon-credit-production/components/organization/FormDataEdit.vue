<template>
	<div id="org-form-data" class="grid grid-cols-12 gap-4 bg-white shadow-sm rounded p-4 text-sm">
		<div class="col-span-6">
			<UILabel :text="$t('organization.create.form.organization_name.th')" :required="true" />
			<UITextInput v-model="form.companyName" :disabled="!edit" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.companyName.required && submitted">{{ $t("organization.create.form_validation.organization_name.th") }}</UIErrorMsg>
		</div>
		<div class="col-span-6">
			<UILabel :text="$t('organization.create.form.organization_name.en')" :required="true" />
			<UITextInput v-model="form.companyNameEn" :disabled="!edit" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.companyNameEn.required && submitted">{{ $t("organization.create.form_validation.organization_name.en") }}</UIErrorMsg>
		</div>
		<div class="col-span-12">
			<UILabel :text="$t('organization.create.form.organization_type')" :required="true" />
			<div class="flex items-center gap-2 w-full">
				<input v-model="form.organization_type" type="radio" name="org-type" :value="1" id="juristic" hidden />
				<input v-model="form.organization_type" type="radio" name="org-type" :value="2" id="government" hidden />

				<label for="juristic">
					<div
						class="px-4 text-center py-2 border"
						:class="{
							'bg-tgo-teal-500 bg-opacity-10 border-tgo-teal-600 text-tgo-teal-600': form.organization_type === 1,
							'bg-white bg-opacity-10': form.organization_type === 0,
						}"
					>
						{{ $t("organization.create.form.juristic") }}
					</div>
				</label>
				<label for="government">
					<div
						class="px-4 text-center py-2 border"
						:class="{
							'bg-tgo-teal-500 bg-opacity-10 border-tgo-teal-600 text-tgo-teal-600': form.organization_type === 2,
							'bg-white bg-opacity-10': form.organization_type === 2,
						}"
					>
						{{ $t("organization.create.form.government") }}
					</div>
				</label>
			</div>
			<UIErrorMsg v-if="!$v.form.organization_type.required && submitted">{{ $t("organization.create.form_validation.organization_type") }}</UIErrorMsg>
		</div>
		<div class="col-span-12">
			<UILabel :text="$t('organization.create.form.fieldOfIndustry')" :required="true" />
			<!-- <UIDropdown v-model="form.organization_type" :disabled="!edit" :option="dropdowns.type" labelAttr="text" /> -->
			<div class="border border-gray-300">
				<UIDropdownSearch v-model="form.fieldOfIndustry" :options="dropdowns.type" valueAttr="value" textAttr="text" :searchable="true" />
			</div>
			<div v-if="form.fieldOfIndustry === 'other'" class="flex items-center gap-2 mt-2 border-l-2 border-tgo-teal-500 px-2">
				<span class="text-sm">{{ $t("organization.create.form.fieldOfIndustryCustom") }} <span class="text-red-500 text-sm">*</span></span>
				<UITextInput v-model="form.fieldOfIndustryCustom" />
			</div>
			<UIErrorMsg v-if="!$v.form.fieldOfIndustryCustom.required_other && submitted">{{ $t("organization.create.form_validation.type_other") }}</UIErrorMsg>

			<UIErrorMsg v-if="!$v.form.fieldOfIndustry.required && submitted">{{ $t("organization.create.form_validation.organization_name.en") }}</UIErrorMsg>
		</div>

		<div class="col-span-12 border-t border-dashed"></div>

		<div class="col-span-5">
			<UILabel :text="$t('organization.create.form.address.th')" :required="true" />
			<UITextInput :disabled="!edit" v-model="form.address" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.address.required && submitted">{{ $t("organization.create.form_validation.address.th") }}</UIErrorMsg>
		</div>
		<div class="col-span-5">
			<UILabel :text="$t('organization.create.form.address.en')" :required="true" />
			<UITextInput :disabled="!edit" v-model="form.addressEn" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.addressEn.required && submitted">{{ $t("organization.create.form_validation.address.en") }}</UIErrorMsg>
		</div>

		<div class="col-span-2">
			<UILabel :text="$t('organization.create.form.village')" :required="false" />
			<UITextInput :disabled="!edit" v-model="form.village" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
		</div>

		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.province')" :required="true" />
			<!-- <UIDropdown v-model="form.province" @input="getDistrict" :disabled="!edit" :option="dropdowns.provinces" labelAttr="text" /> -->
			<div class="border border-gray-300">
				<UIDropdownSearch v-model="form.province" @input="form.district='';form.subDistrict='';getDistrict($event)" :disabled="!edit" :options="dropdowns.provinces" valueAttr="value" textAttr="text" :searchable="true" />
			</div>
			<UIErrorMsg v-if="!$v.form.province.required && submitted">{{ $t("organization.create.form_validation.province") }}</UIErrorMsg>
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.district')" :required="true" />
			<!-- <UIDropdown v-model="form.district" @input="getSubdistrict" :disabled="dropdowns.district.length === 0 && !edit" :option="dropdowns.district" labelAttr="text" /> -->
			<div class="border border-gray-300">
				<UIDropdownSearch v-model="form.district" @input="form.subDistrict='';getSubdistrict($event)" :disabled="dropdowns.district?.length === 0 && !edit" :options="dropdowns.district" valueAttr="value" textAttr="text" :searchable="true" />
			</div>
			<UIErrorMsg v-if="!$v.form.district.required && submitted">{{ $t("organization.create.form_validation.district") }}</UIErrorMsg>
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.subDistrict')" :required="true" />
			<!-- <UIDropdown v-model="form.subDistrict" :disabled="dropdowns.subdistrict.length === 0 && !edit" :option="dropdowns.subdistrict" labelAttr="text" /> -->
			<div class="border border-gray-300">
				<UIDropdownSearch v-model="form.subDistrict" :disabled="dropdowns.subdistrict?.length === 0 && !edit" :options="dropdowns.subdistrict" valueAttr="value" textAttr="text" :searchable="true" />
			</div>
			<UIErrorMsg v-if="!$v.form.district.required && submitted">{{ $t("organization.create.form_validation.subdistrict") }}</UIErrorMsg>
		</div>

		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.road')" :required="false" />
			<UITextInput :disabled="!edit" v-model="form.road" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.landArray')" :required="false" />
			<UITextInput :disabled="!edit" v-model="form.landArray" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.postCode')" :required="true" />
			<UITextInput :disabled="!edit" v-model="form.postCode" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.postCode.required && submitted">{{ $t("organization.create.form_validation.postCode") }}</UIErrorMsg>
		</div>
		<!-- <div class="col-span-12"></div> -->
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.phone')" :required="true" />
			<UITextInput :disabled="!edit" v-model="form.phone" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
			<UIErrorMsg v-if="!$v.form.phone.required && submitted">{{ $t("organization.create.form_validation.phone") }}</UIErrorMsg>
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.fax')" :required="false" />
			<UITextInput :disabled="!edit" v-model="form.fax" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
		</div>
		<div class="col-span-4">
			<UILabel :text="$t('organization.create.form.website')" :required="false" />
			<UITextInput :disabled="!edit" v-model="form.website" customClass="px-2 py-2 border outline-none focus:border-green-500 w-full" />
		</div>

		<div class="col-span-12 grid grid-cols-1 gap-4">
			<div>
				<UILabel :text="form.organization_type === 1 ? $t('openAccount.form.document.verified') : $t('openAccount.form.document.verified1')" ></UILabel>
				<UIFileUpload id="doc-upload-1" @upload="uploadFile($event, 'verified')" :filename="form.document.verified.name"></UIFileUpload>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.authorize')" ></UILabel>
				<UIFileUpload id="doc-upload-2" @upload="uploadFile($event, 'authorize')" :filename="form.document.authorize.name"></UIFileUpload>
			</div>
			<div>
				<UILabel :text="$t('openAccount.form.document.card_id_representative')" ></UILabel>
				<UIFileUpload id="doc-upload-4" @upload="uploadFile($event, 'card_id_representative')" :filename="form.document.card_id_representative.name"></UIFileUpload>
			</div>
		</div>

		<div class="col-span-12"></div>
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import uploadImages from "../../static/mixins/upload-image";

export default {
	props: ["form", "edit", "submitted"],
	mixins: [uploadImages],
	async mounted() {
		console.log(this.form);
		await this.getProvince();
		await this.getDistrict();
		await this.getSubdistrict();

		await this.getType();
	},
	data() {
		return {
			dropdowns: {
				type: [],
				provinces: [],
				district: [],
				subdistrict: [],
			},
			showUpload: false,
		};
	},
	validations() {
		return {
			form: {
				companyName: { required },
				companyNameEn: { required },
				fieldOfIndustry: { required },
				fieldOfIndustryCustom: {
					required_other: (value) => {
						if (value !== "" && this.form.fieldOfIndustry === "other") {
							return true;
						}
						return this.form.fieldOfIndustry !== "other";
					},
				},
				address: { required },
				addressEn: { required },
				province: { required },
				district: { required },
				subDistrict: { required },
				postCode: { required },
				phone: { required },
				organization_type: { required },

			},
		};
	},
	// watch:{
	// 	'form.province'(value){
	// 		// console.log(value);
	// 		this.form.district = ""
	// 		this.form.subDistrict = ""
	// 		this.getDistrict()
	// 	},
	// 	'form.district'(value){
	// 		// console.log(value);
	// 		this.form.subDistrict = ""
	// 		this.getSubdistrict()
	// 	},

	// },
	methods: {
		removeImage() {
			this.form.companyLogo = "";
		},
		async uploadImage(input) {
			const formData = new FormData();
			const fileItem = input.target.files[0];
			// console.log(fileItem);
			formData.append("file", fileItem);
			const resp = await this.uploadImages(formData);
			// console.log(resp);
			this.form.companyLogo = resp.src;
		},
		async uploadFile(input, key) {
			if (input.target.files[0]) {
				const formData = new FormData();
				const fileItem = input.target.files[0];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await this.uploadImages(formData);
				// console.log(resp);
				this.form.document[key] = resp;
			}
		},
		baseUrl(url) {
			return process.env.baseUrl + url;
		},
		async getType() {
			const app = this;
			this.dropdowns.type = await this.$axios
				.$get(`/api/v1/dropdown/organization-type`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getProvince() {
			const app = this;
			this.dropdowns.provinces = await this.$axios
				.$get(`/api/v1/dropdown/provinces`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getDistrict(e) {
			const app = this;
			// console.log("province",e);
			// this.form.district = "";
			// this.form.subDistrict = "";
			this.dropdowns.district = await this.$axios
				.$get(`/api/v1/dropdown/district?province=${this.form.province}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err);
				});
		},
		async getSubdistrict() {
			const app = this;
			// this.form.subDistrict = "";
			this.dropdowns.subdistrict = await this.$axios
				.$get(`/api/v1/dropdown/subdistrict?province=${this.form.province}&district=${this.form.district}`)
				.then((resp) => resp)
				.catch((err) => {
					console.log(err.response.data);
				});
		},
	},
};
</script>

<style>
#org-form-data .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;

	border: 1px solid #e8e8e8 !important;
	border-radius: 0 !important;
	display: flex;
	padding: 6px 0px 6px 0px !important;
	white-space: normal;
}
</style>
