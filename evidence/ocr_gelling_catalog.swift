#!/usr/bin/env swift

import AppKit
import Foundation
import Vision

guard CommandLine.arguments.count == 2 else {
    fputs("usage: ocr_gelling_catalog.swift IMAGE\n", stderr)
    exit(2)
}

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let image = NSImage(contentsOf: url) else {
    fputs("cannot load image\n", stderr)
    exit(2)
}
var proposed = NSRect(origin: .zero, size: image.size)
guard let cgImage = image.cgImage(
    forProposedRect: &proposed,
    context: nil,
    hints: nil
) else {
    fputs("cannot obtain CGImage\n", stderr)
    exit(2)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.recognitionLanguages = ["en-US"]
request.minimumTextHeight = 0.005

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
} catch {
    fputs("Vision OCR failed: \(error)\n", stderr)
    exit(1)
}

let observations = (request.results ?? []).sorted {
    let leftLine = Int((1.0 - $0.boundingBox.midY) * 500.0)
    let rightLine = Int((1.0 - $1.boundingBox.midY) * 500.0)
    if leftLine != rightLine {
        return leftLine < rightLine
    }
    return $0.boundingBox.minX < $1.boundingBox.minX
}
for observation in observations {
    guard let candidate = observation.topCandidates(1).first else {
        continue
    }
    let box = observation.boundingBox
    print(
        String(
            format: "%.6f\t%.6f\t%.6f\t%.6f\t%@",
            box.minX,
            box.minY,
            box.width,
            box.height,
            candidate.string
        )
    )
}
