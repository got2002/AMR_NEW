<template>
	<div class="space-y-3">
		<label class="flex items-start gap-2 text-sm">
			<input :disabled="disable" v-model="form.request_permission" name="requestPermission" :value="0" type="checkbox" class="w-5 h-5 border border-black rounded-0" />
			{{ $t("openAccount.form.request_permission.item1") }}
		</label>
		<label class="flex items-start gap-2 text-sm">
			<input :disabled="disable" v-model="form.request_permission" name="requestPermission" :value="1" type="checkbox" class="w-5 h-5 border border-black rounded-0" />
			{{ $t("openAccount.form.request_permission.item2") }}
		</label>
		<label class="flex items-start gap-2 text-sm">
			<input :disabled="disable" v-model="form.request_permission" name="requestPermission" :value="2" type="checkbox" class="w-5 h-5 border border-black rounded-0" />
			{{ $t("openAccount.form.request_permission.item3") }}
		</label>
	</div>
</template>

<script>
export default {
    props:{
		form:Object,
		disable:{
			type:Boolean,
			default:()=>false
		}
	}
};
</script>

<style>
</style>