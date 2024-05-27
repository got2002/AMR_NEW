<template>
	<div class="flex items-center gap-2">
		<button v-if="!isEdit" @click="isEdit = true">
			<IconEdit customClass="text-yellow-500 w-6 h-6"/>
		</button>
		<input v-model="data.accountName" :title="data.accountName" class="outline-none w-full" :disabled="!isEdit" :class="{ 'outline-none bg-transparent': !isEdit, 'bg-white border px-2 py-1 border-gray-300 focus:border-green-500': isEdit }" />
		<button v-if="isEdit" @click="editName">
			<IconCheck customClass="text-green-500 w-6 h-6"/>
		</button>
        <button v-if="isEdit" @click="isEdit = false">
			<IconXMark/>
		</button>
	</div>
</template>

<script>
export default {
	props: ["data"],
	data() {
		return {
			name: this.data,
			isEdit: false,
		};
	},
    methods:{
        editName(){
            this.$emit('edit',this.data.accountName)
            this.isEdit = false
        }
    }
};
</script>

<style>
</style>