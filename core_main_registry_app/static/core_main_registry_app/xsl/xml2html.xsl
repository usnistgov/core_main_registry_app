<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:rsm="http://schema.nist.gov/xml/res-md/1.0wd-02-2017">
    <xsl:output method="html" indent="yes" encoding="UTF-8" />

    <xsl:template name="title">
        <xsl:choose>
            <xsl:when test="//rsm:Resource/rsm:identity/rsm:title!=''">
                <xsl:value-of select="//rsm:Resource/rsm:identity/rsm:title"/>
            </xsl:when>
            <xsl:otherwise>
                <i>No resource name</i>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="/">
        <div class="container">
            <table class="table table-hover">
                <tr>
                    <td colspan="2">
                        <xsl:variable name="url" select="//rsm:Resource/rsm:content/rsm:landingPage" />
                        <xsl:choose>
                            <xsl:when test="//rsm:Resource/rsm:content/rsm:landingPage!=''">
                                <a target="_blank" rel="noopener noreferrer" href="{$url}" style="font-weight: bold">
                                    <xsl:call-template name="title"/>
                                </a>
                            </xsl:when>
                            <xsl:otherwise>
                                <strong>
                                    <xsl:call-template name="title"/>
                                </strong>
                            </xsl:otherwise>
                        </xsl:choose>
                    </td>
                </tr>
                <xsl:apply-templates select="/*" />
                <xsl:apply-templates select="//*[not(*)]" />
            </table>
        </div>
    </xsl:template>

    <xsl:template match="/*">
        <xsl:apply-templates select="@*"/>
    </xsl:template>

    <xsl:template match="//*[not(*)]">

        <xsl:variable name="name" select="name(.)" />
        <xsl:variable name="value" select="." />

        <xsl:choose>
            <xsl:when test="following-sibling::node()[name()=$name] or preceding-sibling::node()[name()=$name]">
                <xsl:choose>
                    <xsl:when test="preceding-sibling::node()[name()=$name]" >
                    </xsl:when>
                    <xsl:otherwise>
                        <tr>
                            <td style="width: 25%;">
                                <xsl:value-of select="$name" />
                            </td>
                            <td>
                                <span class='value'>
                                    <xsl:call-template name="join">
                                        <xsl:with-param name="current" select="$value" />
                                        <xsl:with-param name="list" select="following-sibling::node()[name()=$name]" />
                                        <xsl:with-param name="separator" select="', '" />
                                    </xsl:call-template>
                                </span>
                            </td>
                        </tr>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>

            <xsl:otherwise>
                <tr>
                    <td style="width: 25%;">
                        <xsl:value-of select="$name" />
                    </td>
                    <td>
                        <span class='value'>
                            <xsl:choose>
                                <xsl:when test="contains($name, 'URL')">
                                    <a target="_blank" rel="noopener noreferrer" href="{$value}"><xsl:value-of select="$value"/></a>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="$value"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </span>
                    </td>
                </tr>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="@*" />
    </xsl:template>

    <xsl:template name="join">
        <xsl:param name="current" />
        <xsl:param name="list" />
        <xsl:param name="separator"/>

        <xsl:value-of select="$current" />
        <xsl:value-of select="$separator" />

        <xsl:for-each select="$list">
            <xsl:value-of select="." />
            <xsl:if test="position() != last()">
                <xsl:value-of select="$separator" />
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:variable name="name" select="name(.)" />
        <xsl:variable name="value" select="." />

        <tr>
            <td width="180">
                <xsl:value-of select="$name" />
            </td>
            <td>
                <span class='value'>
                    <xsl:choose>
                        <xsl:when test="contains($name, 'URL')">
                            <a target="_blank" rel="noopener noreferrer" href="{$value}"><xsl:value-of select="$value"/></a>
                        </xsl:when>
                        <xsl:when test="$name='localid' and $value=''">
                            <i>
                                The Local ID will be automatically generated.
                            </i>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="$value"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
            </td>
        </tr>
    </xsl:template>
</xsl:stylesheet>
