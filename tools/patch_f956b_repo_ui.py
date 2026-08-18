from pathlib import Path

path = Path("app/src/main/java/dev/busung/s25uroot/MainActivity.kt")
text = path.read_text(encoding="utf-8")

old = """    override fun onResume() {\n        super.onResume()\n        if (resumedOnce) installViewModel.refresh() else resumedOnce = true\n    }\n"""
new = """    override fun onResume() {\n        super.onResume()\n        (application as? F956bTestApplication)?.importF956bTestLog()\n        if (resumedOnce) installViewModel.refresh() else resumedOnce = true\n    }\n"""
if old not in text:
    raise SystemExit("MainActivity onResume insertion point not found")
text = text.replace(old, new, 1)

old = """    onStartDownload: (UpdateInfo) -> Unit,\n    onInstall: () -> Unit,\n) {\n    LazyColumn(\n"""
new = """    onStartDownload: (UpdateInfo) -> Unit,\n    onInstall: () -> Unit,\n) {\n    val context = LocalContext.current\n    val f956bTestTarget =\n        device.model.equals(\"SM-F956B\", ignoreCase = true) &&\n            device.kernelRelease == \"6.1.145-android14-11-33418572-abF956BXXS4DZG3\"\n    LazyColumn(\n"""
if old not in text:
    raise SystemExit("OverviewPage insertion point not found")
text = text.replace(old, new, 1)

old = """        item { InstallStatusCard(installState, onInstall) }\n        item { DeviceCard(device) }\n"""
new = """        item { InstallStatusCard(installState, onInstall) }\n        if (f956bTestTarget) {\n            item {\n                F956bTestCard {\n                    context.startActivity(Intent(context, F956bExploitTestActivity::class.java))\n                }\n            }\n        }\n        item { DeviceCard(device) }\n"""
if old not in text:
    raise SystemExit("Overview card insertion point not found")
text = text.replace(old, new, 1)

marker = "\nprivate sealed interface UpdateStatus {\n"
card = r'''

@Composable
private fun F956bTestCard(onClick: () -> Unit) {
    val view = LocalView.current
    val interactionSource = remember { MutableInteractionSource() }
    Card(
        onClick = {
            clickHaptic(view)
            onClick()
        },
        modifier = Modifier.fillMaxWidth(),
        shape = expressiveClickableCardShape(interactionSource),
        interactionSource = interactionSource,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.tertiaryContainer,
            contentColor = MaterialTheme.colorScheme.onTertiaryContainer,
        ),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 18.dp, vertical = 18.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Icon(Icons.Rounded.Security, contentDescription = null, modifier = Modifier.size(38.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text("SM-F956B DZG3 exploit test", style = MaterialTheme.typography.titleMedium)
                Text(
                    "Runs the bundled test payload. After a reboot, reopen this app and export the run from History.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = LocalContentColor.current.copy(alpha = 0.82f),
                )
            }
            Icon(Icons.Rounded.ChevronRight, contentDescription = null)
        }
    }
}
'''
if marker not in text:
    raise SystemExit("UpdateStatus insertion point not found")
text = text.replace(marker, card + marker, 1)

path.write_text(text, encoding="utf-8")
print("patched repository UI with F956B test card and history refresh")
