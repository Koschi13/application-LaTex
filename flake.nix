{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = (import nixpkgs) {
          inherit system;
        };

          tex = (pkgs.texlive.combine {
            inherit (pkgs.texlive)
              adjustbox
              arydshln
              babel-german
              collectbox
              currfile
              datetime
              eso-pic
              etoolbox
              filecontents
              filehook
              fmtcount
              fontawesome5
              fontaxes
              infwarerr
              koma-script
              lastpage
              layouts
              lipsum
              marvosym
              microtype
              moderncv
              multirow
              opensans
              pdflscape
              pdfpages
              pdftexcmds
              pgf
              picture
              scheme-basic
              setspace
              tabu
              ucs
              varwidth
              xcolor
              xkeyval
              ;
          });
      in {
        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            #texliveFull
            tex
            texstudio
          ];
        };
      }
    );
}
