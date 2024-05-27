<template>
	<div class="relative" v-clickOutside="()=>openDropdown = false">
		<div @click="openDropdown = !openDropdown" class="bg-white px-4 py-2 shadow-sm rounded flex items-center justify-between gap-4 border cursor-pointer">
			<div class="flex items-center gap-2">
				<div class="w-3 h-3  rounded-full"
                    :class="{
                        'bg-green-500':value === 'Registered',
                        'bg-red-500':value === 'Cancelled',
                        'bg-gray-500':value === 'Expired',
                    }"
                ></div>
				{{ dropdownText(value) }}
			</div>
			<IconArrowDown />
		</div>
		<div v-if="openDropdown" class="absolute z-10 top-11 left-0 w-full bg-white shadow-md border rounded text-sm">
			<div @click="seletectOption('Registered')" class="px-2 py-1 hover:bg-gray-100 cursor-pointer flex items-center gap-2">
				<div class="w-3 h-3 bg-green-500 rounded-full"></div>
				{{ $t("project.view_page.registered") }}
			</div>
			<div @click="seletectOption('Cancelled')" class="px-2 py-1 hover:bg-gray-100 cursor-pointer flex items-center gap-2">
				<div class="w-3 h-3 bg-red-500 rounded-full"></div>
				{{ $t("project.view_page.cancelled") }}
			</div>
			<div @click="seletectOption('Expired')" class="px-2 py-1 hover:bg-gray-100 cursor-pointer flex items-center gap-2">
				<div class="w-3 h-3 bg-gray-500 rounded-full"></div>
				{{ $t("project.view_page.expired") }}
			</div>
		</div>
	</div>
</template>

<script>
import vClickOutside from "v-click-outside";
export default {
    directives: {
		clickOutside: vClickOutside.directive,
	},
	props: {
		value: {
			default: () => "",
		},
	},
	data: () => {
		return {
			openDropdown: false,
		};
	},
	methods: {
		dropdownText(value) {
			switch (value) {
				case "Registered":
					return this.$t("project.view_page.registered");

				case "Cancelled":
					return this.$t("project.view_page.cancelled");
				case "Expired":
					return this.$t("project.view_page.expired");
			}
		},
		seletectOption(value) {
			this.$emit("input", value);
			this.openDropdown = false;
		},
	},
};
</script>

<style>
</style>