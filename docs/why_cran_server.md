# Why You Should Run Your Own CRAN Server

## Introduction
We’re excited to release our solution for R internal package distribution, `cran-server`. In this post, we’ll explain why this project could be valuable for your team, discuss some of the alternatives available and help you get started.

## Benefits
### Internal Packages
Packages are an integral part of the R ecosystem. Even relatively new R users will likely be familiar with loading external code by running commands like `install.packages(‘ggplot2’)` or `library(data.table)`. As Hadley Wickham writes [“in R, the fundamental unit of shareable code is the package”](http://r-pkgs.had.co.nz/intro.html). R packages can be tremendously useful [even if you don’t share code](https://hilaryparker.com/2014/04/29/writing-an-r-package-from-scratch/), but we believe that lowering the barriers to writing and sharing R packages amongst team members can have a positive impact beyond the traditional benefits of code reuse.

[As our colleague, Stephanie Kirmer,  has spoken about](https://github.com/skirmer/odsc2018/), embracing a practice of internal R package development on your team facilitates reproducibility, improves productivity and helps break down information silos. R-users who are building models and performing analyses are able to be more productive than they would be on their own because they can rely on code that’s already tested and documented rather than repeating common tasks. By capturing common processes, documentation and best-practices into knowledge-transfer artifacts, R packages speed up the onboarding process for new analytics professionals and empower other members of the organization.

### `cran-server`
Most organizations that use R will have at least some code and/or packages they want to distribute among their members, but not publicly. This means that the easiest way for team members to install R packages – the public R Package Repository, [CRAN](https://cran.r-project.org/) – won’t work for them. Since we think that writing internal packages is so valuable, we wrote an application to simplify and streamline internal package distribution.

We think that `cran-server` offers some compelling features that make it a good choice:
* Users install internal packages the same way they’d install anything on CRAN, without the need for any external plugins or packages: `install.packages`.
* It saves versioned artifacts that are easy to find and install, improving reproducibility.
* It can be easily deployed in any environment that can run containers and it doesn’t require the ability to mount volumes for data persistence.
* Its completely free and open source.

### Alternatives
There are plenty of other ways to distribute packages to your team members, although each had some drawbacks for R that led us to develop `cran-server`:

#### Distribute via Version Control (VCS) such as git, svn, etc.

We’ve found that using a package repository provides several nice benefits over distributing code with VCS alone (though development work should absolutely still be done in VCS).
* Versioning: Good and convenient versioning is critical when it comes to reproducibility. If team members want to re-run an analysis or if a job is scheduled to run to retrain a model, they shouldn’t have to manually checkout a bunch of git tags across several repositories, or worse – have to find specific untagged old commits. By having a repository of versioned artifacts, reproducibility becomes much more straightforward.
* Dependency Resolution: Admittedly, Public CRAN [has its faults](https://mran.microsoft.com/timemachine) when it comes to resolving package dependencies. However, `cran-server` allows users to leverage familiar (base R!) tooling to resolve internal dependencies automatically. Doing this using VCS alone would either involve custom tooling or complex `Makefile` installation processes.
  * Though not necessary, `cran-server` also supports hosting versions of packages from public CRAN. Because many packages only enforce minimum dependency versions, it is often easy to get surprised by breaking changes in external dependencies. By freezing the versions of external packages that your team uses in `cran-server` you can minimize the risk of public package updates breaking your code and instead update carefully on your schedule.

#### Store packages on a networked file system or an FTP server
As described in the [official documentation](https://cran.r-project.org/doc/manuals/R-admin.html#Setting-up-a-package-repository), it is possible to just use a networked file system or an FTP server. Choosing NFS or FTP, however, requires you or your organization to maintain your own infrastructure. `cran-server` _can_ be run on-prem on a single server and it can also just as easily be run on a cluster or in the cloud using object storage like [Amazon S3](https://aws.amazon.com/s3/) and services such as [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/) or [Amazon ECS](https://aws.amazon.com/ecs/). Further, we find releasing packages through the `cran-server` Web API to be a more sustainable system than managing files directly like you would on an FTP server. The API automatically takes care of steps like validating the artifact and updating package manifests, simplifying the process for users and maintainers. 

#### Use a paid service like [Rstudio Package Manager](https://www.rstudio.com/products/package-manager/) 
Rstudio Package Manager is new and appears to have a few very promising features. Though, it is a young, paid, closed-source solution. `cran-server` has been running internally at Uptake for nearly 2 years, serving thousands of downloads and over 60 packages. And, it’s free, lightweight and [open source](https://github.com/UptakeOpenSource/cran-server)!

#### Use an Artifact repository like [Nexus](https://www.sonatype.com/nexus-repository-sonatype) or [Artifactory](https://jfrog.com/artifactory/)
Artifact Repositories like Nexus and Artifactory are popular for serving Docker Images, Jars, and Javascript and Python Packages – and they do it well. Though there are some third-party plugins available, there isn’t first-class support for R in either of them. While both offer docker deployment options, neither seem to support persistence to cloud object storage automatically.

## Getting Started
[Check out the quickstart!](https://github.com/UptakeOpenSource/cran-server/)
