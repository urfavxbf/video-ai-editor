/**
 * Approved landscape composition geometry for UrFavXBF + PIX.
 *
 * Both PORTRAIT HEADS (no full-body overlays) are now ~35% bigger than V2:
 * from 306×346 to 414×468 pixels in a 1920×1080 composition.
 * The center chart/caption safe column stays unobstructed.
 */
export const PORTRAIT_LAYOUT = {
  canvasWidth: 1920,
  canvasHeight: 1080,
  top: 202,
  left: 64,
  right: 64,
  width: 414,
  height: 468,
  centerLeft: 515,
  centerRight: 1405,
  footerBottom: 40,
} as const;
export const PORTRAIT_SCALE_V3 = 414 / 306;
