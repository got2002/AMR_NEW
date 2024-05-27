<template>
	<td class="py-2 text-center font-light">
		{{ text }}
	</td>
</template>

<script>
	export default {
		props: {
            text:{
                type:String,
                default:()=>''
            },
            align:{
                type:String,
                default:()=>'center'
            },
            
        },
	};
</script>

<style></style>
