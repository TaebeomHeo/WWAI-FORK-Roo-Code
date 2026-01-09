import React from "react"
import { Mode, getAllModes } from "@roo/modes"
import { useExtensionState } from "@/context/ExtensionStateContext"
import { useAppTranslation } from "@/i18n/TranslationContext"
import { cn } from "@/lib/utils"

interface ModeSelectorPromptProps {
	mode: Mode
	setMode: (value: Mode) => void
}

export const ModeSelectorPrompt = ({ mode, setMode }: ModeSelectorPromptProps) => {
	const { customModes, customModePrompts } = useExtensionState()
	const { t } = useAppTranslation()

	const modes = React.useMemo(() => {
		const allModes = getAllModes(customModes)

		return allModes.map((m) => ({
			...m,
			description: customModePrompts?.[m.slug]?.description ?? m.description,
		}))
	}, [customModes, customModePrompts])

	return (
		<div className="flex flex-col gap-3 w-full px-2">
			<h3 className="text-sm font-medium text-vscode-foreground opacity-90">
				{t("chat:modeSelector.title")}
			</h3>
			<div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
				{modes.map((m) => {
					const isSelected = m.slug === mode
					return (
						<div
							key={m.slug}
							onClick={() => setMode(m.slug)}
							className={cn(
								"flex flex-col gap-1 p-3 rounded-md border cursor-pointer transition-all",
								"hover:bg-vscode-list-hoverBackground hover:border-vscode-focusBorder",
								isSelected
									? "bg-vscode-list-activeSelectionBackground border-vscode-focusBorder text-vscode-list-activeSelectionForeground"
									: "bg-vscode-editor-background border-vscode-dropdown-border text-vscode-foreground"
							)}>
							<div className="flex items-center justify-between">
								<span className="font-bold text-sm">{m.name}</span>
								{isSelected && <span className="codicon codicon-check opacity-80" />}
							</div>
							{m.description && (
								<span className={cn(
									"text-xs line-clamp-2",
									isSelected ? "text-vscode-list-activeSelectionForeground opacity-90" : "text-vscode-descriptionForeground"
								)}>
									{m.description}
								</span>
							)}
						</div>
					)
				})}
			</div>
		</div>
	)
}
