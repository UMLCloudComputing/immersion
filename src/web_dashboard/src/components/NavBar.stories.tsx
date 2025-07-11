import type { Meta, StoryObj } from '@storybook/react';
import { NextAuthProvider } from "../../.storybook/NextAuthProvider"
import { fn } from '@storybook/test';

import { NavBar } from './NavBar';
import React, { FC } from 'react';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
    title: 'Example/NavBar',
    component: NavBar,
    parameters: {
        nextjs: {
            appDirectory: true
        }
        // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/configure/story-layout
    },
    decorators: [
        (Story) => (
            <NextAuthProvider>
                <Story />
            </NextAuthProvider>
        )
    ],
    // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
    tags: ['autodocs'],
    // More on argTypes: https://storybook.js.org/docs/api/argtypes
    //   argTypes: {
    //     backgroundColor: { control: 'color' },
    //   },
    // Use `fn` to spy on the onClick arg, which will appear in the actions panel once invoked: https://storybook.js.org/docs/essentials/actions#action-args
    //   args: { {data}: {data} Guild[] },
} satisfies Meta<typeof NavBar>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/writing-stories/args
export const Primary: Story = {

};
