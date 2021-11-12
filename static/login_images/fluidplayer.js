fluidPlayer("video-id", {
  layoutControls: {
    controlBar: {
      autoHideTimeout: 3,
      animated: true,
      autoHide: true,
    },
    htmlOnPauseBlock: {
      html: null,
      height: null,
      width: null,
    },
    autoPlay: true,
    mute: false,
    allowTheatre: false,
    playPauseAnimation: true,
    playbackRateEnabled: true,
    allowDownload: true,
    playButtonShowing: true,
    fillToContainer: true,
    posterImage: "../assets/img/profile.jpg",
  },
  vastOptions: {
    adList: [
      {
        roll: "preRoll",
        vastTag: "#",
        adText: "Advertisement",
      },
    ],
    adCTAText: true,
    adCTATextPosition: "top",
  },
});
