import { expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import GetData_opt from "../GetData_opt.vue";


test('GetData.vue mount test', async () => {
    expect(GetData_opt).toBeTruthy();
    const wrapper = mount(GetData_opt);
    expect(wrapper.find('#msg').exists()).toBe(false);
    await wrapper.get('#btn').trigger('click');
    expect(wrapper.find('#msg').exists()).toBe(true);
    expect(wrapper.get('#msg').text()).toBe("This should exist now.");
})