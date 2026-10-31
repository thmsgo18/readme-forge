// Lists on-screen app windows with their CoreGraphics id, for `screencapture -l <id>`.
// Usage: swift list_windows.swift [app-name-filter]
import CoreGraphics
let owner = CommandLine.arguments.count > 1 ? CommandLine.arguments[1].lowercased() : ""
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []
for w in list where (w["kCGWindowLayer"] as? Int) == 0 {
    let name = w["kCGWindowOwnerName"] as? String ?? ""
    if owner.isEmpty || name.lowercased().contains(owner) {
        let b = w["kCGWindowBounds"] as? [String: Any] ?? [:]
        print("\(w["kCGWindowNumber"] ?? 0)\t\(name)\t\(w["kCGWindowName"] as? String ?? "")\t\(b["Width"] ?? 0)x\(b["Height"] ?? 0)")
    }
}
